function [ accuracy, cm ] = evaluateModel( model, data, classes )
%EVALUATEMODEL Evaluates the performance of the model
%   Evaluates the performance of the model using a data set and a class set
%   where the class set consists of the correct classes for each data
%   vector in the data set.

    % score count
    score = 0;
    % number of data vectors
    s = size(data, 1);
    % classification result (initialized to zeros)
    classout = zeros(s, 1);
    
    for i = 1:size(data, 1),
        % predicted class by the model
        prediction = predict(model, data(i,:));
        classout(i) = prediction;
        % the actual class
        actual = classes(i);
        % increase the score if the prediction was correct
        if prediction == actual,
            score = score + 1;
        end
    end
    accuracy = score/s;
    % disp([num2str(100*score/s) '%, '  num2str(score) ' out of ' num2str(s)]);
    cm = confusionmat(classes, classout);
    % disp(cm);
end

