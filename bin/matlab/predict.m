for j = 1:size(TDMS, 2),
    data = TDMS{j}.data;
    
    % make data binary
%     data = sign(data);
    % perform tf-idf
    data = tfidf2(data);
    
    classes = CLASSES{j}.data;
    % binary classes
    % {1, 2} -> 0
    % {2, 3} -> 1
    binclasses = round((classes -1) /3);
    
    
    [ devdata, traindata, testdata ] = splitdata(data);
    [ devclasses, trainclasses, testclasses ] = splitdata(binclasses);

    
    model = fitcknn(devdata, devclasses(:,1), 'NumNeighbors', 3, 'Distance', 'cosine');
%     model = fitcknn(devdata, devclasses(:,1), 'NumNeighbors', 3, 'Distance', 'spearman');
    disp('Prior');
    disp(model.Prior);
    
    score = 0;
    s = size(traindata, 1);
    classout = zeros(s, 1);
    for i = 1:size(traindata, 1),
        prediction = predict(model, traindata(i,:));
        classout(i) = prediction;
        actual = trainclasses(i, 1);
        if prediction == actual,
            score = score + 1;
        end
    end
    disp([num2str(100*score/s) '%, '  num2str(score) ' out of ' num2str(s)]);
    cm = confusionmat(trainclasses(:,1), classout);
    disp(cm);
end

