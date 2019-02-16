//Script -- export to CSV

$("#csv").click(function() {
 	    $.ajax({
            type : "POST",
            url : "/json2csv",
            dataType : "json",
            traditional: true,
            success: function(data) {
                    var finalVal = ''
                    finalVal =  'Activity_type,Center,Role,Activities Completed,experience_challenge,buffer1,buffer2,buffer3,challenge_handle_situation,conducted by,could_improved,curriculum,end_date,end_time,feedback,hashtag,logdate,logtime,student_performance,start_date,start_time,student_objectives,todays_objective,topics_covered,upload,went_well' + '\n';
                    for (var i = 0; i < data.length; i++) {
                        var value = data[i];
                        for (var j = 0; j < value.length; j++) {
                            var innerValue = value[j];
                            var result = innerValue.replace(/"/g, '""');
                            if (result.search(/("|,|\n)/g) >= 0)
                                result = '"' + result + '"';
                            if (j > 0)
                                finalVal += ',';
                                finalVal += result;
                        }

                        finalVal += '\n';
                    }
                 var download = function(content, fileName, mimeType) {
                         var a = document.createElement('a');
                         mimeType = mimeType || 'application/octet-stream';

                        if (navigator.msSaveBlob) { // IE10
                            navigator.msSaveBlob(new Blob([content], {
                                type: mimeType
                            }), fileName);
                        }
                        else if (URL && 'download' in a)
                        { //html5 A[download]
                            a.href = URL.createObjectURL(new Blob([content], {
                                   type: mimeType
                            }));
                            a.setAttribute('download', fileName);
                            document.body.appendChild(a);
                            a.click();
                            document.body.removeChild(a);
                        }
                        else
                        {
                            location.href = 'data:application/octet-stream,' + encodeURIComponent(content); // only this mime type is supported
                        }
                    }
                    download(finalVal, 'dowload.csv', 'text/csv;encoding:utf-8');
            }
       });
});

//End Script -- export to CSV


//script - filter the table

    $(document).ready(function(){
    $('.filterable .btn-filter').click(function(){
        var $panel = $(this).parents('.filterable'),
        $filters = $panel.find('.filters input'),
        $tbody = $panel.find('.table tbody');
        if ($filters.prop('disabled') == true) {
            $filters.prop('disabled', false);
            $filters.first().focus();
        } else {
            $filters.val('').prop('disabled', true);
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });

    $('.filterable .filters input').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var $input = $(this),
        inputContent = $input.val().toLowerCase(),

        $panel = $input.parents('.filterable'),
        column = $panel.find('.filters th').index($input.parents('th')),
        $table = $panel.find('.table'),
        $rows = $table.find('tbody tr');
        /* Dirtiest filter function ever ;) */
        var $filteredRows = $rows.filter(function(){
            var value = $(this).find('td').eq(column).text().toLowerCase();
            var first_char = value.substring(0, inputContent.length)
            return first_char.indexOf(inputContent) === -1;
        });
        /* Clean previous no-result if exist */
        $table.find('tbody .no-result').remove();
        /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
        $rows.show();
        $filteredRows.hide();
        /* Prepend no-result row if all rows are filtered */
        if ($filteredRows.length === $rows.length) {
            $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">No result found</td></tr>'));
        }
    });
});

//End script - filter the table
