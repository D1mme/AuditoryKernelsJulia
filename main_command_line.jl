# Example:  julia main_command_line.jl "TIMIT" "TIMIT_train.csv" 0.008 1

import Pkg 
Pkg.activate(".")
import FFTW
using Random
using FileIO: load, save, loadstreaming, savestreaming
using LinearAlgebra
using Plots
using WAV
include("mp_utils.jl")  # Load the file
import .mp_utils
include("filter_utils.jl")
import .filter_utils
using Base.Threads
using TickTock

import DSP
using CSV, DataFrames
using JLD2


##  Input arguments 
ID = ARGS[1] #"TIMIT" 
csv_file = ARGS[2] #"TIMIT_train.csv"
exp_threshold = parse(Float64, ARGS[3])
nEpochs = parse(Int, ARGS[4])

if length(ARGS)<5
    continue_flag = false	
    count_start = 0
else
    continue_flag = true
    count_start = parse(Int, ARGS[5])
end

##  Function for plotting
function arrayPlot(kernels, ID::String, count::Int)
    Ng = length(kernels)  # Number of kernels
    rows, cols = 4, 8     # Define layout size
    max_plots = rows * cols
    Ng = min(Ng, max_plots)  # Prevent exceeding 32 subplots

    # Construct the file path where the figure will be saved
    dir_name = "Results_" * ID
    file_name = "figure_" * string(count) * ".svg"
    file_path = joinpath(dir_name, file_name)

    if !isdir(dir_name)
        mkdir(dir_name)
    end
    
    # Create plot with a more tightly packed layout
    p = plot(
        layout=(rows, cols),  # 4x8 grid layout
        size=(1200, 600),      # Figure size (adjust as needed)
        margin=0.5Plots.mm,    # Tight margin to reduce whitespace
        padding=0.5Plots.mm,   # Reducing padding between subplots
        legend=false,          # Disable legend for clarity
        showaxis=false,        # Hide axes to save space
        framestyle=:none,      # No borders for each plot
    )

    # Add each kernel as a subplot (adjusting subplot numbers to fit)
    for j in 1:Ng
        plot!(p, kernels[j].kernel, subplot=j, showaxis=false, legend=false)
    end

    # Save the plot to the specified file as SVG
    savefig(p, file_path)

    println("Plot saved to: ", file_path)  # Print where the file is saved
    p = nothing	
end

## Function for saving result
function save_to_jld2(ID::String, count::Int, MPparam, Filterparam, csv_file::String, rs, kernels)
    # Create directory if it doesn't exist
    dir_name = "Results_" * ID
    if !isdir(dir_name)
        mkdir(dir_name)
    end

    # Construct file path
    file_name = "kernels_" * string(count) * ".jld2"
    file_path = joinpath(dir_name, file_name)

    # Save variables to JLD2 file
    @save file_path MPparam Filterparam csv_file count rs kernels

    println("Saved to: ", file_path)
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
    20000,      # max_iter
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
for nEpoch in 1:nEpochs
    # Shuffle directory
    df = CSV.read(csv_file, DataFrame)
    shuffled_paths = shuffle(df.file_path)

    #Inner loop
    for path in shuffled_paths
        if count - 1 < count_start
            count += 1
        else
            println(count)

            # Load audio
            println(path)
            x, fs_read = wavread(path)
            fs_read = Int(fs_read)
            if fs_read > Filterparam.fs
                println("resampling")
                x = DSP.Filters.resample(x, Filterparam.fs//fs_read, dims=1)
            end
            x = DSP.Filters.filt(f, x)
            x = x/maximum(abs.(x))

            # Run MP and gradient update
            x_res, kernel_list, amp_list, index_list, norm_list = mp_utils.matching_pursuit(x, MPparam.stop_type, MPparam.stop_cond, kernels, nothing, MPparam.max_iter)
            mp_utils.update_kernels!(index_list, kernel_list, amp_list, kernels, x_res, MPparam.step_size, MPparam.smoothing_weight)
            
            # Trim and expand the kernels every so often
            if mod(count, MPparam.exp_update) == 0
                mp_utils.trim_and_expand_kernels!(kernels, MPparam.exp_threshold, MPparam.exp_range)
            end

            # Plot and store results every so often
            global count += 1
            if mod(count, 10) == 0
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
