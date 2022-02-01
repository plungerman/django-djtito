function formatdate(date) {

  var d = new Date();
  var weekday = new Array(7);
  weekday[0]=  "Sunday";
  weekday[1] = "Monday";
  weekday[2] = "Tuesday";
  weekday[3] = "Wednesday";
  weekday[4] = "Thursday";
  weekday[5] = "Friday";
  weekday[6] = "Saturday";

  var n1 = weekday[d.getDay()];

  var d = new Date();
  var month = new Array();
  month[0] = "January";
  month[1] = "February";
  month[2] = "March";
  month[3] = "April";
  month[4] = "May";
  month[5] = "June";
  month[6] = "July";
  month[7] = "August";
  month[8] = "September";
  month[9] = "October";
  month[10] = "November";
  month[11] = "December";
  var n2 = month[d.getMonth()];

  var hours = date.getHours();
  var minutes = date.getMinutes();
  var day = date.getDay();
  var month = date.getMonth();
  var date = date.getDate();
  var ampm = hours >= 12 ? 'p.m.' : 'a.m.';
  hours = hours % 12;
  hours = hours ? hours : 12; // the hour '0' should be '12'
  minutes = minutes < 10 ? '0'+minutes : minutes;
  var strDate = hours + ':' + minutes + ' ' + ampm + ' on ' + n1 + ', ' + n2 + ' ' + date;
  return strDate;
}

var $dateandtime = $('#dateandtime');

function updateDateAndTime() {
  var date = formatdate(new Date());
  $dateandtime.text(date);
}

setInterval(updateDateAndTime, 1000 * 60);
updateDateAndTime();
