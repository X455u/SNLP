%% Read the data from files

tdmfiles = {'../../data/tdm1.csv'; '../../data/tdm2.csv'};
classfiles = {'../../data/classes1.csv'; '../../data/classes2.csv'};

delimiterIn = ',';
headerlinesIn = 1;

TDMS = {};
for i = 1:size(tdmfiles, 1),
   TDMS{i} = importdata(tdmfiles{i}, delimiterIn, headerlinesIn);
end
CLASSES = {};
for i = 1:size(classfiles, 1),
   CLASSES{i} = importdata(classfiles{i}, delimiterIn, headerlinesIn);
end
