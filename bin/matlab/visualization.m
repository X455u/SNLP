data = A.data;
m = squeeze(mean(data, 1));

jsonfile = fopen('../../data/words.json', 'w');
jsonlen = 100;

dim = 4;

% reduce dimensions
[plotData, eigenV] = pcaDimReduct(data, dim);

scatter3(...
    plotData(:, 1),...
    plotData(:, 2),...
    plotData(:, 3),...
    repmat(30, size(plotData,1), 1),...
    plotData(:,4)...
);
% print labels for data points
% text(plotData(:,1) + 0.1,...
%     plotData(:,2) + 0.1,...
%     plotData(:,3) + 0.1,...
%     num2str((1:size(data,1))','%d')...
% );

% write occurences to json list
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
