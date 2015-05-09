cmapredtogreen = [
    [1, 0, 0];
    [0.75, 0.25, 0];
    [0.75, 0.25, 0];
    [0.25, 0.75, 0];
    [0.25, 0.75, 0];
    [0, 1, 0];
];

for j = 1:size(TDMS, 2),
    data = TDMS{j}.data;
    classes = CLASSES{j}.data;
    % m = squeeze(mean(data, 1));

    dim = 3;
    % reduce dimensions
    [plotData, eigenV] = pcaDimReduct(data, dim);

    figure(j);
    scatter3(...
        plotData(:, 1),...
        plotData(:, 2),...
        plotData(:, 3),...
        repmat(30, size(plotData,1), 1),...
        arrayfun(@(x) x-1,classes(:,1)),...
        'filled'...
    );
    colormap(cmapredtogreen);
    colorbar;
    %print labels for data points
%     text(plotData(:,1) + 0.1,...
%         plotData(:,2) + 0.1,...
%         plotData(:,3) + 0.1,...
%         num2str((1:size(data,1))','%d')...
%     );

    % write occurences to json list
    jsonfile = fopen('../../data/words.json', 'w');
    jsonlen = 100;
    [occur, indices] = sort(sum(data), 'descend');
    fprintf(jsonfile,'[\n');
    for i = 1:jsonlen,
       str = sprintf('["%s", %d]', A.textdata{indices(i)}, occur(i));
       if i ~= jsonlen,
           fprintf(jsonfile, '%s,\n', str);
       else
           fprintf(jsonfile, '%s\n]\n', str);
       end
    end    
end

