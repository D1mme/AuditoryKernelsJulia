# AuditoryKernelsJulia
Reproduce Smith and Lewicky

# Usage:
`julia main_command_line.jl "TIMIT" "TIMIT_train.csv" 0.008 1`

This will run `main_command_line.jl` and create a folder `Results_TIMIT`. The folder `Results_TIMTI` contains a plot of the kernels (per 10 iterations) and a `.jld2` file containing the learned kernels, the gradient, and the total number of updates (in terms of the sum of the amplitude). It will run for `1` epoch, and the shrinking and expanding of the kernels hapens based on the `0.008`. There are more parameters inside `main_command_line.jl`. 

One can continue training by adding the number of the last save:
`julia main_command_line.jl "TIMIT" "TIMIT_train.csv" 0.008 1 510`

The code will look for `Results_TIMIT/kernels_510.jld2` and continue the training from there. 


 
 
