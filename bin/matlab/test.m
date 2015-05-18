% Best will be:
% tdm: 1, data type: tfidf, classIndex:  1, neighbors: 5, distance: correlation
% set parameters and run with test data

disp('TESTING');
tdmIndex = 1;
clsIndex = 1;
neighbors = 5;
distance = 'correlation';

data = tfidf2(TDMS{tdmIndex}.data')';
classes = CLASSES{tdmIndex}.data(:,clsIndex);
binclasses = round((classes - 1) / 3);

[ devdata, traindata, testdata ] = splitdata(data);
[ devclasses, trainclasses, testclasses ] = splitdata(binclasses);

model = fitcknn(...
    devdata, devclasses,...
    'NumNeighbors', neighbors,...
    'Distance', distance...
);

[accuracy, cm] = evaluateModel(model, testdata, testclasses);
tp = cm(2,2);
fp = cm(1,2);
tn = cm(1,1);
fn = cm(2,1);
precision = tp / (tp + fp);
recall = tp / (tp + fn);
trueNegRate = tn / (tn + fp);
fmeasure = (2 * precision * recall) / (precision + recall);
mcc = (tp * tn - fp * fn) / sqrt((tp + fp)*(tp + fn)*(tn + fp)*(tn + fn));

disp([...
    'MCC: ' num2str(mcc) ', '...
    'F-Measure: ' num2str(fmeasure) ', '...
    'Accuracy: ' num2str(100*accuracy) '%, '...
    'Precision: ' num2str(100*precision) '%, '...
    'Recall: ' num2str(100*recall) '%, '...
    'True negative rate: ' num2str(100*trueNegRate) '%'...
]);
disp(cm);
