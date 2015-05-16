% Reading the data
filename = 'data1/tdm1.csv';
delimiterIn = ',';
headerlinesIn = 1;
A = importdata(filename,delimiterIn,headerlinesIn);


% SOM
x = A.data';
net = selforgmap([6 7]); % 6 x 7 SOM
net = train(net,x); % training neural network
view(net)
y = net(x);
classes = vec2ind(y); 

% Plot SOM sample hits
plotsomhits(net,x)

% Plot SOM neighbor distances
plotsomnd(net)

