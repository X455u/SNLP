function [ dataOut, eigenVectors ] = pcaDimReduct( dataIn, dim )
%pcaDimReduct Reduces the dimension using PCA
%   Takes a data matrix (with row vectors) and a integer value describing
%   the number of dimentions the data should be reduced to. The function
%   returns a data matrix with reduced dimension and the eigen vectors used
%   in the process.

% calculate mean values
m = mean(dataIn, 1);
% normalize vectors
X = bsxfun(@minus, dataIn, m);
% covariance matrix for X
covariancex = (X'*X)./(size(X, 1) - 1);
% eigenvectors and diagonal matrix with eigen values
[V, ~] = eigs(covariancex, dim);

dataOut = X * V;
eigenVectors = V;

end

