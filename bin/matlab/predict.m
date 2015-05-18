dataTypes = {'tf'; 'binary'; 'tfidf'; 'pca'};
neighborNums = [1; 3; 5; 7];
distances = {
    'cityblock'; 'chebychev'; 'correlation'; 'cosine'; 'euclidean';
    'hamming'; 'jaccard'; 'minkowski'; 'spearman'
};

bestScore = -1;
bestCm = [0 0; 0 0];
bestParameters = '';

disp('TRAINING');

for tdmIndex = 1:size(TDMS, 2),
    for dataTypeIndex = 1:size(dataTypes, 1),
        for clsIndex = 1:size(CLASSES{tdmIndex}.data, 2),
            for neighborIndex = 1:size(neighborNums, 1),
                for distanceIndex = 1:size(distances, 1),
                    
                    data = TDMS{tdmIndex}.data;
                    
                    dataType = dataTypes{dataTypeIndex};
                    if strcmp(dataType, 'binary'),
                        data = sign(data);
                    elseif strcmp(dataType, 'tfidf'),
                        data = tfidf2(data')';
                    elseif strcmp(dataType, 'pca'),
                        [data, ~] = pcaDimReduct(data, 10);
                    end

                    classes = CLASSES{tdmIndex}.data(:,clsIndex);
                    % binary classes
                    % {1, 2} -> 0
                    % {2, 3} -> 1
                    binclasses = round((classes - 1) / 3);

                    neighbors = neighborNums(neighborIndex);
                    
                    distance = distances{distanceIndex};

                    [ devdata, traindata, testdata ] = splitdata(data);
                    [ devclasses, trainclasses, testclasses ] = splitdata(binclasses);

                    currentParameters = [
                        'tdm: ' num2str(tdmIndex) ', '...
                        'data type: ' dataType ', '...
                        'classIndex:  ' num2str(clsIndex) ', '...
                        'neighbors: ' num2str(neighbors) ', '...
                        'distance: ' distance ...
                    ];
                    disp(currentParameters);
                    
                    model = fitcknn(...
                        devdata, devclasses,...
                        'NumNeighbors', neighbors,...
                        'Distance', distance...
                    );
                    % disp('Prior');
                    % disp(model.Prior);

                    [accuracy, cm] = evaluateModel(model, traindata, trainclasses);
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
                    % disp(cm);
                    
                    if mcc > bestScore,
                        bestParameters = currentParameters;
                        bestScore = mcc;
                        bestCm = cm;
                    end
                    
                end
            end
        end
    end
end

disp('TRAINING DONE');
disp('Best parameters:');
disp(bestParameters);
disp(bestScore);
