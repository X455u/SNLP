%% Reading the data
filename = 'data1/tdm1.csv';
delimiterIn = ',';
headerlinesIn = 1;
A = importdata(filename,delimiterIn,headerlinesIn);


%% SOM
x = A.data';
net = selforgmap([6 7]);
net = train(net,x);
view(net)
y = net(x);
classes = vec2ind(y);

