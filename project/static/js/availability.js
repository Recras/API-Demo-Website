var availableDates;

Date.prototype.yyyymmdd = function() {                           
        var yyyy = this.getFullYear().toString();                                    
        var mm = (this.getMonth()+1).toString(); // getMonth() is zero-based         
        var dd  = this.getDate().toString();             
                            
        return yyyy + '-' + (mm[1]?mm:"0"+mm[0]) + '-' + (dd[1]?dd:"0"+dd[0]);
   };  


function onlineBoekingDateAvailable(date)
{
  if ($.inArray(date.yyyymmdd(), availableDates) != -1){ 
      return [true, ""];
  } else {
      return [false,"","Helaas geen plekken meer beschikbaar"]; 
  }
}

$(document).ready(function()
{
    var div = $('#arrangementbeschikbaarheid');
    div.addClass('nozebra');
    $.getJSON(div.attr('href'), function(data) {
        availableDates  = data['results'];
        
        div.text('');
        div.datepicker({
            dateFormat:       'yy-mm-dd',
            firstDay:         1,
            showWeek:         true,
            numberOfMonths:   3,
            beforeShowDay:    onlineBoekingDateAvailable,
            minDate:          -0, 
            maxDate:          "+2M +10D"
        },
        $.datepicker.regional['nl']
        );          
    });
});
