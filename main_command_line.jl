# Example:  julia main_command_line.jl "TIMIT" "TIMIT_train.csv" 0.008 4000

import Pkg 
Pkg.activate(".")
import FFTW
using Random
using LinearAlgebra
using Plots
using WAV
include("mp_utils.jl")  # Load the file
import .mp_utils
include("filter_utils.jl")
import .filter_utils
using Base.Threads

import DSP
using CSV, DataFrames
using JLD2


##  Input arguments 
ID = ARGS[1] #"TIMIT" 
csv_file = ARGS[2] #"TIMIT_train.csv"
exp_threshold = parse(Float64, ARGS[3])
nIts = parse(Int, ARGS[4])


## This is to keep the loop going till nIts is reached.
maxEpochs = 1000 

## This decides how often data is stored
nStore = 10

## If there are 5 arguments we continue from a previous run
if length(ARGS)<5
    continue_flag = false	
    count_start = 0
else
    continue_flag = true
    count_start = parse(Int, ARGS[5])
end


println("Number of threads: ", Threads.nthreads())
println(pwd())


##  Set user parameters
# matching pursuit
MPparam = mp_utils.MPparams(
    32,         # Ng
    100,        # kernel_size
    10,         # random_seed
    "amplitude",# stop_type
    0.1,        # stop_cond
    40000,      # max_iter
    0.005,      # step_size
    0.7,        # smoothing_weight
    exp_threshold,      # exp_threshold (ARGS[3])
    1/10,       # exp_range
    50          # exp_update
)


# filter
Filterparam = filter_utils.Filterparams(
    100,        # f_low
    6000,       # f_high
    16000,      # fs
    256,        # length_filter
    1024,       # length_freq_ax (plotting only)
)


# Window for kernel initialisation
window = DSP.Windows.hamming(100)


## Prepare program
# Set random seed
Random.seed!(MPparam.random_seed)


# Get filter
f = filter_utils.getFIRbandpassfilter(Filterparam.f_low, Filterparam.f_high, Filterparam.fs, Filterparam.length_filter)
filter_utils.plotFIRresponse(f, Filterparam.fs, Filterparam.length_freq_ax)


# Initialise kernels
global count = 0
kernels = []
for _ in 1:MPparam.Ng
    kernel = window.*randn(MPparam.kernel_size)               # Generate a random kernel of size (100,)
    kernel /= norm(kernel)
    gradient = zeros(MPparam.kernel_size)             # Initialize the gradient as zeros of size (100,)
    abs_amp = 0.0                     # Initialize absolute amplitude to 0.0 (or any other value)
    
    # Add the kernel object to the kernels list
    push!(kernels, mp_utils.Kernel(kernel, gradient, abs_amp))
end


# If continue_flag: load old kernels (the reason we still initialised them is for the random seed)
if continue_flag
    dir_name = "Results_" * ID
    file_name = "kernels_" * ARGS[5] * ".jld2"
    file_path = joinpath(dir_name, file_name)
    data = load(file_path, "kernels")
    kernels = [mp_utils.Kernel(d.kernel, d.gradient, d.abs_amp) for d in data]
end


# Main loop
arrayPlot(kernels, ID, count)
for nEpoch in 1:maxEpochs
    # Shuffle directory
    df = CSV.read(csv_file, DataFrame)
    shuffled_paths = shuffle(df.path_wav)

    #Inner loop
    for path in shuffled_paths
        flush(stdout)

        if count - 1 < count_start
            count += 1
        else
            println(count)

            # Load audio
            println(path)
            succesLoadFlag = true
            try
                x, fs_read = wavread(path)
            catch e
                println("Failed reading path printed above")
                succesLoadFlag = false
            end
            
            if succesLoadFlag
                fs_read = Int(fs_read)
                if fs_read > Filterparam.fs
                    println("resampling")
                    x = DSP.Filters.resample(x, Filterparam.fs//fs_read, dims=1)
                    x = DSP.Filters.filt(f, x)
                end
            
                x = x/maximum(abs.(x))

                # Run MP and gradient update
                x_res, kernel_list, amp_list, index_list, norm_list = mp_utils.matching_pursuit(x, MPparam.stop_type, MPparam.stop_cond, kernels, nothing, MPparam.max_iter)
                mp_utils.update_kernels!(index_list, kernel_list, amp_list, kernels, x_res, MPparam.step_size, MPparam.smoothing_weight)
                
                # Trim and expand the kernels every so often
                if mod(count, MPparam.exp_update) == 0
                    mp_utils.trim_and_expand_kernels!(kernels, MPparam.exp_threshold, MPparam.exp_range)
                end

                # Plot and store results every so often
                count += 1
                if mod(count, nStore) == 0
                    # (1): store
                    rs = deepcopy(Random.GLOBAL_RNG)
                    save_to_jld2(ID, count, MPparam, Filterparam, csv_file, rs, kernels)
                    
                    # (2): plot
                    arrayPlot(kernels, ID, count)
                end
                
                x = nothing
                x_res = nothing
                kernel_list = nothing
                amp_list = nothing
                index_list = nothing
                norm_list = nothing
            end
        end
    end
end
