function [ dev, train, test ] = splitdata( D )
%SPLITDATA Splits the data into development, training and test
% rows are documents, columns are terms
% from our term document matrices, use A.data

devp = 0.7;
trainp = 0.2;
% testing gets the rest

cols = size(D,1);

% Counting column lengths
devam = round(devp * cols);
trainam = round(trainp * cols);
testam = cols - (devam + trainam);

% Splitting the data
dev = D(1:devam,:);
train = D(devam+1:devam+trainam,:);
test = D(devam+trainam+1:cols,:);

end

