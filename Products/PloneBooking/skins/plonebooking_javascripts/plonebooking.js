
function ID(id) { return document.getElementById(id); }

function getXmlHttpRequest() {
    var ajaxobject = null;
    if ( window.XMLHttpRequest ) {
        ajaxobject = new XMLHttpRequest();
    } else if ( window.ActiveXObject ) {
        ajaxobject = new ActiveXObject( 'Microsoft.XMLHTTP' );
    } else {
        ajaxobject = null;
    }
    return ajaxobject
}

function showPeriodicityResult(url, alt_url, target_id, form_id, waiting_text) {
    ajaxobject = getXmlHttpRequest();

    form = document.getElementById(form_id);
    periodicity_type = getPeriodicityType(form);
    periodicity_end_date = form['periodicity_end_date'].value;
    periodicity_variable = form['periodicity2_x'].value;

    query = getPeriodicityQuery(periodicity_type, periodicity_end_date, periodicity_variable);
    url = url + query + "&d=" + (new Date()).getTime();
    alt_url = alt_url + query;

    // Opera does not support ajax
    if (ajaxobject == null) {
        window.location = alt_url;
    } else {
        var node = document.getElementById(target_id);
        node.innerHTML = waiting_text;
        ajaxobject.open('GET', url, true);
        ajaxobject.onreadystatechange = function() {CallBackGenerateAjaxHTML(ajaxobject, target_id);}
        ajaxobject.send(null);
    }
}

function getPeriodicityQuery(periodicity_type, periodicity_end_date, periodicity_variable) {
    query = '&periodicity_type=' + periodicity_type_value + '&periodicity_end_date=' + periodicity_end_date
    if (periodicity_variable != null) {
        query = query + '&periodicity_variable=' + periodicity_variable;
    }
    return query
}

function getPeriodicityType(form) {
    periodicity_type = form['periodicity_type'];
    periodicity_type_value = null;
    for (i = 0; i < periodicity_type.length; i++) {
        obj = periodicity_type[i];
        if (obj.checked == true) {
            periodicity_type_value = obj.value;
        }
    }
    return periodicity_type;
}

function toggleFieldset(e) {
    e = e || window.event;
    node = e.target || e.srcElement;

    while (node && node.nodeName != 'FIELDSET')
        node = node.parentNode;

    if (node)
        node.className = node.className == 'opened' ? 'closed': 'opened';
}

function CallBackGenerateAjaxHTML(ajaxobject, target_id) {
    if (ajaxobject.readyState == 4) {
        if (ajaxobject.status > 299 || ajaxobject.status < 200) {
            return;
        }
        elem = document.getElementById(target_id);
        elem.innerHTML = ajaxobject.responseText;
    }
}

/* Create bookings one by one from the periodicity results and display a progress bar  */
function createThoseBookings(url) {
    var progressBar = document.getElementById("bookingProgressbar");
    var lstBookings = document.getElementById("lstBookings");
    var bookings = lstBookings.getElementsByTagName("input");
    var createBookings = document.getElementById("createBookings");
    lstBookings.style.display = "none";
    createBookings.style.display = "none";
    progressBar.parentNode.style.display = "block";
    document.location.href = document.URL.split('#')[0] + "#secondStep";

    var xhReq; var index = 0; var nbBooked = 0; var nbAlreadyBooked = 0;
    var getResponse = function () {
        if (xhReq.readyState != 4)
            return null;
        if (xhReq.responseText == "OK")
                ++nbBooked;
            if (xhReq.responseText == "NOK")
                ++nbAlreadyBooked;
        xhReq.onreadystatechange = function() {};
        var percentage = Math.round(100 * ++index / bookings.length) + "%";
        progressBar.firstChild.style.width = percentage;
        progressBar.lastChild.firstChild.data = percentage;
            if (index == bookings.length) {
                var doneButton = document.getElementById("goto-booking");
                var bookingsDone = document.getElementById("bookingsDone");
                var txt = bookingsDone.firstChild.data;
                txt = txt.replace('%created%', nbBooked);
                txt = txt.replace('%already_booked%', (nbAlreadyBooked));
                txt = txt.replace('%errors%', (bookings.length - (nbBooked + nbAlreadyBooked)))
                bookingsDone.firstChild.data = txt;
                bookingsDone.style.display = "block";
                doneButton.style.display = "block";
                return null;
            }
        sendRequest(index);
    }
    var sendRequest = function() {
        var ts = bookings[index].value.split("_");
        var parameters = "start_ts=" + ts[0] + "&end_ts=" + ts[1] + "&d=" + (new Date()).getTime();
        xhReq = getXmlHttpRequest();
            xhReq.open('GET', url + "?" + parameters , true);
            xhReq.onreadystatechange = getResponse;
        xhReq.send(null);
    }
    sendRequest();
}


function modifyStatusOnThoseBookings(container_url, here_id, action, all) {
    var progressBar = document.getElementById("bookingProgressbar");
    var lstBookings = document.getElementById("lstBookings");
    var bookings = lstBookings.getElementsByTagName("input");
    lstBookings.parentNode.parentNode.style.display = "none";
    progressBar.parentNode.style.display = "block";
    document.location.href = document.URL.split('#')[0] + "#progressBarAnchor";

    // Get booking ids
    var booking_ids = new Array();
    for (var i=0; i < bookings.length; i++)
        if (bookings[i].name == 'ids:list') {
            booking_id = bookings[i].value;
            booking_checked = bookings[i].checked ? true : false;

            if (all || booking_checked) {
                booking_ids.push(booking_id);
            }
    }

    if (all) {
        booking_ids.push(here_id);
    }

    var xhReq;
    var index = 0;
    var nbProcessed = 0;
    var nbTotal = booking_ids.length;

    var getResponse = function () {
        if (xhReq.readyState != 4)
            return null;
        if (xhReq.status == 200)
            ++nbProcessed;
        xhReq.onreadystatechange = function() {};
        var percentage = Math.round(100 * ++index / nbTotal) + "%";
        progressBar.firstChild.style.width = percentage;
        progressBar.lastChild.firstChild.data = percentage;
        if (index == nbTotal) {
                var doneButton = document.getElementById("goto-booking");
                if (all && action == 'cancel') {
                    doneButton = document.getElementById("goto-bookableobject");
                }
            var bookingsDone = document.getElementById("bookings-done");
            var txt = bookingsDone.firstChild.data;
            txt = txt.replace('%processed%', nbProcessed);
            txt = txt.replace('%errors%', (nbTotal - nbProcessed));
            bookingsDone.firstChild.data = txt;
            bookingsDone.style.display = "block";
            doneButton.style.display = "block";
            return null;
        }
        sendRequest(index);
    }
    var sendRequest = function() {
        var booking_id = booking_ids[index];
        var parameters = "?d=" + (new Date()).getTime();
        xhReq = getXmlHttpRequest();
        xhReq.open('GET', container_url + "/" + booking_id + "/content_status_modify?workflow_action=" + action, true);
        xhReq.setRequestHeader("raiseError", "False");
        xhReq.onreadystatechange = getResponse;
        xhReq.send(null);
    }
    sendRequest();
}


function sendAjaxRequest(url, func, target) {
    if (target) {
        target.className += " disabled";
        addClassName(document.body, 'wait');
    }
    xhReq = getXmlHttpRequest();
    xhReq.open('GET', url, true);
    /*xhReq.setRequestHeader("raiseError", "False");*/
    xhReq.onreadystatechange = function() {
        if (xhReq.readyState != 4) return null;
        xhReq.onreadystatechange = function() {};
        if (typeof func != 'undefined') func(xhReq);
        if (target)
            target.className = target.className.replace(/ disabled/, "");
        removeClassName(document.body, 'wait');
    };
    xhReq.send(null);

    return false;
}



Timeline = function(content, start_ts, length_ts, action) {
    var cursor = null;
    var start_x;
    var start_left;
    var start_width;
    var day_start = start_ts * 1000;
    var day_length = length_ts * 1000;
    var quarter = day_length / 900 / 1000;
    var container = ID(content);
    var cursor_action = action;
    var timestampInfo = null;

    container.onmousemove = onmousemove;
    container.onmousedown = onmousedown;

    anchors = container.getElementsByTagName('A');
    for (i = 0;i < anchors.length;++i) {
        anchors[i].onselectionstart = function() { return false; }
        anchors[i].onfocus = function() { return false; }
    }

    function displayTimeInterval() {
        formatTime = function (i) { return i < 10 ? '0'+i : i; }

        ts = getTimestamps();
        cs_ts = getClientToServerTimestamp();
        start_ts = ts[0] + cs_ts + 499; // Add +499ms to display 17:00:00 instead of 16:59:59
        end_ts = ts[1] + cs_ts + 499; // Add +499ms to display 17:00:00 instead of 16:59:59
        dt = new Date(start_ts);
        start = formatTime(dt.getHours()) + ':' + formatTime(dt.getMinutes()) + ':' + formatTime(dt.getSeconds());
        dt = new Date(end_ts);
        end = formatTime(dt.getHours()) + ':' + formatTime(dt.getMinutes()) + ':' + formatTime(dt.getSeconds());
        pos = getPosition(cursor);
        timestampInfo.style.top  = pos[1] + cursor.offsetHeight +  'px';
        timestampInfo.style.left = pos[0] + 'px';
        timestampInfo.innerHTML =  "<div>" +  start + " / " + end +"</div>"
        timestampInfo.style.display = 'block';
    }

    function getTimestamps() {
        start_ts = day_start + (parseFloat(cursor.style.left) / 100 * day_length);
        end_ts = start_ts + (parseFloat(cursor.style.width) / 100 * day_length);
        return [ start_ts, end_ts ];
    }

    function getClientToServerTimestamp() {
    var server_ts = parseInt(ID('booking-edit-start-ts').value) * 1000;
    var client_date = new Date(ID('booking-edit-start-date').value);
    var client_ts = client_date.getTime();
    return client_ts - server_ts;
  }

    function onmousemove(e) {
        e = e || window.event;
        var target = e.target || e.srcElement;
        if (target.nodeName == 'DIV') target = target.parentNode;
        if (!cursor && target.parentNode.className == 'timeline') {
            var left = getPosition(target)[0];
            var x = e.clientX || e.screenX;
            var right = left + target.offsetWidth + 3;
            var width = target.offsetWidth;
            target.style.cursor =
                (x >= left  && x <= (left  + 8)) ? 'w-resize' :
                (x <= right && x >= (right - 5)) ? 'e-resize' : 'move';
        }
        return false;
    }

    function onmousedown(e) {
        e = e || window.event;
        target = e.target || e.srcElement;
        if (target.nodeName == 'DIV') target = target.parentNode;
        if (target.parentNode.className == 'timeline') {
            cursor = target;
            cursor.onclick = function() { return false; };
            start_x = e.screenX;
            start_left = parseFloat(cursor.style.left);
            start_width = parseFloat(cursor.style.width);
            timestampInfo = document.body.appendChild(
                document.createElement('DIV')
            );
            timestampInfo.className = 'booking-popup timestamp-info';
            jQuery('body').bind('mousemove', onresize);
            jQuery('body').bind('mouseup', onmouseup);
            displayTimeInterval();
        }
        return false;
    }

    function onresize(e) {
        e = e || window.event;
        var x = e.screenX;
        document.body.style.cursor = cursor.style.cursor;
        move = (x - start_x) / cursor.parentNode.offsetWidth;
        move = Math.floor(move * quarter) / quarter;
        move *= 100;
        if ((start_left + move) < 0 && cursor.style.cursor != 'e-resize')
            move = -start_left;
        if ((start_left + start_width + move) > 100)
            move = 100 - (start_left + start_width);
        switch (cursor.style.cursor) {
            case 'w-resize':
                if ((start_width - move) < (100 / quarter))
                    return false;
                cursor.style.left  = (start_left  + move) + '%';
                cursor.style.width = (start_width - move) + '%';
                break;
            case 'e-resize':
                if ((start_width + move) < (100 / quarter))
                    return false;
                cursor.style.width = (start_width + move) + '%';
                break;
            case 'move':
                cursor.style.left = (start_left + move) + '%';
                break;
        }
        displayTimeInterval();
        return false;
    }

    function onmouseup(e) {
        e = e || window.event;
        e.cancelBubble = true;

        jQuery('body').unbind('mouseup', onmouseup);
        jQuery('body').unbind('mousemove', onresize);
        jQuery('body').bind('mouseup', onmousemove);

        document.body.style.cursor = cursor.style.cursor = 'default';
        addClassName(document.body, 'wait');
        document.body.removeChild(timestampInfo);

        ts = getTimestamps();
        start_ts = Math.round(ts[0] / 1000);
        end_ts = Math.round(ts[1] / 1000);
        sendAjaxRequest(cursor.href + '/testBookingPeriod?start_ts='+start_ts+'&end_ts='+end_ts,
            function(xhReq) {
                if (xhReq.responseText != "True") {
                    lines = xhReq.responseText.split('\n');
                    if (lines.length > 1)
                        alert(lines[1]);
                    ts = lines[0].split(':');
                    cursor.style.left  = start_left + '%';
                    cursor.style.width = start_width + '%';
                } else {
                   // Update start_ts and end_ts hidden fields
		           var node =  ID('booking-start-ts');

		           if (node)
		               node.value = start_ts;

		           var node =  ID('booking-end-ts');

		           if (node)
		               node.value = end_ts;

                }
                cursor = null;
                removeClassName(document.body, 'wait');
            },
            cursor
        );
        return false;
    }
}

var Booking = {
    view             : null,
    form             : null,
    popup            : null,
    start_ts         : null,
    length_ts        : null,
    isBookableObject : function (link) {
        return link.className.match(/(^|\s)bookableObject($|\s)/)
    },

    /* Getters for combo box values */
    getSelectedValue: function(node) {
       return node ? node.options[node.selectedIndex].value : null;
    },
    getType: function() {
       return this.getSelectedValue(Booking.form.btype);
    },
    getCategory: function() {
       return this.getSelectedValue(Booking.form.bcategory);
    },
    getBookableObject: function() {
       return Booking.form.bookableobject.value;
    },
    getDisplayMode: function() {
        return Booking.form.dmode.value;
    },
    getDisplayView: function() {
        return Booking.form.dview.value;
    }
};

Booking.init = function(){
    document.body.style.cursor = "";
    Booking.view = ID('plonebooking-view');
    Booking.form = ID('booking-form');
    if (!Booking.form) {
        return false;
    }
    window.onunload = Booking.closePopup;
    Booking.start_ts = parseInt(Booking.form.start_ts.value);
    Booking.length_ts = parseInt(Booking.form.length_ts.value);
    Booking.displayCalendar();

    if (ID('listing-menu')) {
        var anchors = ID('listing-menu').getElementsByTagName('A');
        for (i = 0;i < anchors.length;++i)
            anchors[i].onclick = Booking.updateDisplayView;
    }
    if (ID('calendar-menu')) {
        var anchors = ID('calendar-menu').getElementsByTagName('A');
        for (i = 0;i < anchors.length;++i)
            anchors[i].onclick = Booking.updateDisplayView;
    }
    if (ID('plonebooking-nav')) {
        var anchors = ID('plonebooking-nav').getElementsByTagName('A');
        for (i = 0;i < anchors.length;++i)
            anchors[i].onclick = Booking.gotoURL;
    }
    if (ID('week-days')) {
        var anchors = ID('week-days').getElementsByTagName('A');
        for (i = 0;i < anchors.length;++i)
            anchors[i].onclick = Booking.gotoURL;
    }
    if (ID('bookingCalendar') || ID('bookingPlanning')) {
        var a_nodes = ID('bookingCalendar') ?
            ID('bookingCalendar').getElementsByTagName('a') :
            ID('bookingPlanning').getElementsByTagName('a');
        for (var i=0; i<a_nodes.length; i++) {
            var a_node = a_nodes[i];
            if (   a_node.className == 'booking-pending'
                  || a_node.className == 'booking-booked'
                  || a_node.className == 'BookingThumb')
                a_node.onclick = Booking.infoPopup;
            else if (   a_node.className.match(/(^|\s)bookIt($|\s)/))
                a_node.onclick = Booking.editPopup;
            else if (a_node.parentNode.className == 'monthBookingCell'
                      || a_node.className == "WeekNumber")
                a_node.onclick = Booking.gotoURL;
        }
        if (ID('bookingPlanning'))
            new Timeline(
                'bookingPlanning',
                Booking.start_ts,
                Booking.length_ts,
                Booking.infoPopup);
    }

    var fieldsets = Booking.form.getElementsByTagName('fieldset');
    for (var i = 0;i < fieldsets.length;++i) {
        if (fieldsets[i].className == 'opened' ||
            fieldsets[i].className == 'closed')
            fieldsets[i].getElementsByTagName('legend')[0].onclick = toggleFieldset;
    }
}

Booking.showOnLoad = function() {
    var query_vars = Booking.parseURL(document.location.href);
    if (query_vars['show:boolean'] == 'True') {
        Booking.refresh(Booking.getCurrentURL(), false);
    }
}

Booking.parseURL = function(url) {
    // Parse query string
    var url_split = url.split('?');
    var query = url_split[(url_split.length - 1)];
    var query_vars = {};
    var query_split = query.split("&");
    for (var i=0;i<query_split.length;i++) {
        var pair = query_split[i].split("=");
        query_vars[pair[0]] = pair[1];
    }
    return query_vars;
}

Booking.refresh = function (url) {
    if (Booking.popup)
        Booking.closePopup();

    var query_vars = Booking.parseURL(url);
    var query = url.replace('?', '/booking_ajax_view?');
    addClassName(document.body, 'wait');
    return sendAjaxRequest(query,
        function (xhReq) {
            ID('plonebooking-view').innerHTML = xhReq.responseText;
            var refresh_filter = false;

            if (query_vars['ts'] && Booking.form.ts.value != query_vars['ts'])
                Booking.form.ts.value = query_vars['ts'];
                var calendar_date = new Date();
                calendar_date.setTime(parseInt(Booking.form.ts.value)*1000);
                Booking.calendar.setDate(calendar_date);
            if (query_vars['dview'] && Booking.form.dview.value != query_vars['dview'])
                Booking.form.dview.value = query_vars['dview'];
                Booking.refreshDisplayViewSelection();

            if (Booking.form['refresh-filter'] || !refresh_filter) {
                Booking.init();
            } else {
                Booking.refreshFilter(false);
            }
        }
    );
};

Booking.openPopup = function (target, properties) {
    var url     = properties['href'] || target.href;
    var content = document.body.appendChild(
        document.createElement('DIV')
    );
    content.className = 'booking-popup';
    if (Booking.popup)
        Booking.closePopup();
    Booking.popup = content;
    sendAjaxRequest(url,
        function(xhReq) {
            pos = getPosition(target);
            content.innerHTML = xhReq.responseText;
            content.style.visibility = 'hidden';
            content.style.display = 'block';
            centerContent(content);
            content.style.visibility = 'visible';
            if (properties['oncomplete'])
                properties['oncomplete'](xhReq);
        },
        target
    );
    return false;
};

Booking.closePopup = function() {
    if (Booking.popup)
        document.body.removeChild(Booking.popup);
    document.body.onscroll = window.onresize = null;
    Booking.popup = null;
    return false;
};

Booking.bookableObjectDescriptionPopup = function(e) {
    e = e || window.event;
    target = e.target || e.srcElement;
    itm = target;
    while (itm.nodeName != 'A') itm = itm.parentNode;
    url = itm.href;
    Booking.openPopup(target, { href: url });
    return false;
}

Booking.infoPopup = function(e) {
    e = e || window.event;
    target = e.target || e.srcElement;
    itm = target;
    while (itm.nodeName != 'A') itm = itm.parentNode;
    url = itm.href + '/booking_info_popup';
    Booking.openPopup(target, { href: url });
    return false;
};

Booking.gotoURL = function(e) {
    var e = e || window.event;
    var target = e.target || e.srcElement;
    var url = null;

    if (target.nodeName == 'A') {
        url = target.href;
    } else {
        url = Booking.getCurrentURL();
    }

    return Booking.refresh(url);
};

/*

*/

Booking.refreshCategory = function(category) {
  Booking.form.bcategory.value = category;
  Booking.form.btype.value = '';
  Booking.form.bookableobject.value = '';
  Booking.refreshFilter(true);
  return false;
}

Booking.refreshType = function(type) {
  Booking.form.btype.value = type;
  Booking.form.bcategory.value = '';
  Booking.form.bookableobject.value = '';
  Booking.refreshFilter(true);
  return false;
}

Booking.refreshDisplayViewSelection = function() {

    if (ID('calendar-menu')) {
        var anchors = ID('calendar-menu').getElementsByTagName('A');
    } else
    if (ID('listing-menu')) {
        var anchors = ID('listing-menu').getElementsByTagName('A');
    }

    var pattern = 'dview=' + Booking.form.dview.value;

    for (var i=0; i<anchors.length; ++i) {
        var anchor = anchors[i];
        removeClassName(anchor, 'selected');

        if (anchor.href.search(pattern) != -1) {
            addClassName(anchor, 'selected');
        }
    }
}

Booking.updateDisplayView = function(e) {
    var e = e || window.event;
    var target = e.target || e.srcElement;

        var itm = target;
        while (itm && itm.nodeName != 'A')
            itm = itm.parentNode;

    var query_vars = Booking.parseURL(itm.href);

        if (query_vars['dview'])
            Booking.form.dview.value = query_vars['dview'];

    Booking.refreshDisplayViewSelection();

    if (!Booking.form['refresh-filter'])
        Booking.refresh(Booking.getCurrentURL(), false);

    return false;
}

Booking.getCurrentURL = function() {
  var url = Booking.form.center_url.value;

  if (Booking.getBookableObject())
    url += '/' + Booking.getBookableObject();

  url += '?ts=' + Booking.form.ts.value;
  url += '&dmode=' + Booking.form.dmode.value;
  url += '&dview=' + Booking.form.dview.value;
  if (Booking.form.btype)
      url += '&btype=' + Booking.form.btype.value;
  if (Booking.form.bcategory)
      url += '&bcategory=' + Booking.form.bcategory.value;
  if (Booking.form.bookableobject)
      url += '&bookableobject=' + Booking.form.bookableobject.value;
  url += '&refresh-filter=1';
  return url;
}

Booking.getNonAuthenticatedURL = function() {
  var url = Booking.form.center_url.value;
  url += '?ts=' + Booking.form.ts.value;
  url += '&dmode=' + Booking.form.dmode.value;
  url += '&dview=' + Booking.form.dview.value;
  if (Booking.form.btype)
      url += '&btype=' + Booking.form.btype.value;
  if (Booking.form.bcategory)
      url += '&bcategory=' + Booking.form.bcategory.value;
  if (Booking.form.bookableobject)
      url += '&bookableobject=' + Booking.form.bookableobject.value;
  url += '&show:boolean=True';
  return url;
};

Booking.editPopup = function (e) {
    if (Booking.form.isAnon.value == "True") {
        document.location.href = Booking.form.portal_url.value + "/login_form?came_from=" + escape(Booking.getNonAuthenticatedURL());
        return false;
    }
    var e = e || window.event;
    var target = e.target || e.srcElement;
    var url = target.href;
    if (!target.nodeName == 'A')
        return ;
    if (target.className.match(/(^|\s)bookIt($|\s)/)
     && !Booking.isBookableObject(target)) {
      url = url.replace(/\/[^/]*[?]/, '/booking_ajax_form?');
        if (Booking.form.btype.value)
            url += '&btype=' + Booking.form.btype.value;
        if (Booking.form.bcategory.value)
            url += '&bcategory=' + Booking.form.bcategory.value;

        Booking.openPopup(target, { href:  url } );
    } else  {
        if (target.className.match(/(^|\s)bookIt($|\s)/))
          url = url.replace(/\/[^/]*[?]/, '/plonebooking_add?ajax=yes&');
        else
          url = url.replace('/edit','/booking_ajax_form');
        Booking.openPopup(target, {
            href: url,
            oncomplete: function() {
                frm = document.forms['booking_form_ajax'];
                Booking.creation = frm.obj_url.value;
                new Timeline('bookingPlanningEdit', frm.cal_start_ts.value, frm.day_length.value);

                var periodicitySetup = document.getElementById('periodicitySetup');
                if (periodicitySetup) {
                  periodicitySetup.className = 'closed';
                  var legend = periodicitySetup.getElementsByTagName('legend')[0];
                  legend.onclick = toggleFieldset;
                }
                frm.fullName.focus();
            },
            position: 'center'
        });
    }
    return false;
};

Booking.periodicityPopup = function(e) {
    if (Booking.form.isAnon.value == "True") {
        document.location.href = Booking.form.portal_url.value + "/login_form?came_from=" + escape(Booking.getNonAuthenticatedURL());
        return false;
    }
    var e = e || window.event;
    var target = e.target || e.srcElement;
    var url = target.href.replace('_form', '_ajax_form');
    if (!target.nodeName == 'A')
        return ;

    Booking.openPopup(target, { href:  url } );

    return false;
}

Booking.submit = function (e) {
    e = e || window.event;
    target = e.target || e.srcElement;
    data = "";
    inputs = target.getElementsByTagName("input");

    for (i = 0;i < inputs.length;++i)
        if (inputs[i].type == "text" || (inputs[i].type == "hidden" && inputs[i].className != "doNotSubmit"))
            data += "&" + inputs[i].name + "=" + inputs[i].value;

    inputs = target.getElementsByTagName("textarea");

    for (i = 0;i < inputs.length;++i)
        data += "&" + inputs[i].name + "=" + inputs[i].value;

    data = data.substring(1);
    xhReq = getXmlHttpRequest();
    xhReq.open('POST' , target.action, true);
    xhReq.setRequestHeader('Content-type', 'application/x-www-form-urlencoded');
    xhReq.onreadystatechange = function() {
        if (xhReq.readyState != 4) return null;
        if (xhReq.responseText != 'True') {
            response = xhReq.responseText;
            if (response.split('\n').length > 1)
                ID('booking_form_ajax_errors').innerHTML =
                    response.substring(response.indexOf('\n') + 1);
                ID('booking_form_ajax_errors').style.display = 'block';
        } else {
            Booking.creation = null;
            Booking.closePopup();
            Booking.refresh(Booking.getCurrentURL());
        }
    };
    xhReq.send(encodeURI(data));
    return false;
};


Booking.cancel = function (booking_url) {
    sendAjaxRequest(
        Booking.creation + '/updateStatus?workflow_action=cancel',
        function (xhReq) {
            Booking.creation = null;
            Booking.closePopup();
        }
    );
}


/*
    Ajax function to retract this booking
*/
Booking.remove = function (target) {
    Booking.applyToAll(target, function(itm) { itm.className += ' disabled'; });
    url = target.href.replace('content_status_modify', 'updateStatus');
    sendAjaxRequest(url,
        function(xhReq) {
            if (xhReq.readyState != 4) return null;
            Booking.applyToAll(target, function(itm) {
                cell = itm.parentNode;
                if (itm.className == 'BookingThumb' || cell.nodeName == 'SPAN') {
                    cell.parentNode.removeChild(cell);
                    cell = null;
                } else
                    cell.removeChild(itm);
                if (cell && !cell.getElementsByTagName('A').length
                         && cell.getElementsByTagName('INPUT').length) {
                    var currentPath = Booking.form.center_url.value.replace(/[?].*$/, '');
                    ts = cell.getElementsByTagName('INPUT')[0].value.split(':');
                    link = document.createElement('A');
                    link.innerHTML = '+';
                    link.className = 'visualNoPrint bookIt';
                    if (!Booking.form.bookableobject.value)
                        link.href = currentPath + '/plonebooking_add';
                    else {
                        link.className += ' bookableObject';
                        link.href = currentPath + '/' + Booking.form.bookableobject.value + '/plonebooking_add_form';
                    }
                    link.href += '?start_ts='+ts[0]+'&end_ts='+ts[1];
                    link.onclick = Booking.editPopup;
                    cell.appendChild(link);
                }
            });
        },
        target
    );
    Booking.closePopup();
    return false;
}

/*
    ajax function to validate booking
*/
Booking.validate = function (target) {
    Booking.applyToAll(target, function(itm) { itm.className += ' disabled'; });
    url = target.href.replace('content_status_modify', 'updateStatus');
    sendAjaxRequest(url,
        function(xhReq) {
            if (xhReq.readyState != 4) return null;
            Booking.applyToAll(target,
                function(itm) { itm.className = 'booking-booked'; }
            );
        },
        target
    );
    Booking.closePopup();
    return false;
}

Booking.displayCalendar = function(){
    var container = document.getElementById('filter-calendar');
    if (container && !container.childNodes.length) {
        var timestamp = parseInt(Booking.form.ts.value)*1000;
        Booking.calendar = new Calendar(1, timestamp, Booking.onCalendarSelect);
        Booking.calendar.create(container);
        Booking.calendar.show();
    }
}
/*
    apply the same function on every booking cell in the calendar view
*/
Booking.applyToAll = function (target, func, content) {
    var node = content ? ID(content) : ID('bookingCalendar') || ID('bookingPlanning');
    if (!node) return;
    var booking_url = target.href.replace(/(.*)[/].*/, "$1");
    var a_nodes = node.getElementsByTagName('a');
    for (var i=0; i < a_nodes.length; i++)
        if (a_nodes[i].href == booking_url)
            func(a_nodes[i]);
}

/*
    Only refresh the booking filter part
*/
Booking.refreshFilter = function(refresh_view) {
    if (refresh_view == null) {
        var refresh_view = true;
    }

    var url = Booking.form.center_url.value;

    var type_node = Booking.form.btype;
    if (type_node.value && type_node.options) {
        var type_value = type_node.options[type_node.selectedIndex].value;
    } else {
        var type_value = type_node.value;
    }

    if (Booking.form.bcategory) {
        var category_node = Booking.form.bcategory;
        if (type_node.value && type_node.options) {
            var category_value = category_node.options[category_node.selectedIndex].value;
        } else {
            var category_value = category_node.value;
        }
    }
    
    else category_value = '';

    var bookableobject_node = Booking.form.bookableobject;
    if (bookableobject_node.value && bookableobject_node.options) {
        var bookableobject_value = bookableobject_node.options[bookableobject_node.selectedIndex].value;
    } else {
        var bookableobject_value = bookableobject_node.value;
    }

    var view_value = Booking.form.dview.value;
    var mode_value = Booking.form.dmode.value;

    url += '/booking_filter?btype=' + type_value  +
            '&bcategory=' + category_value +
            '&bookableobject=' + bookableobject_value +
            '&dmode=' + mode_value +
            '&dview=' + view_value;

    sendAjaxRequest(url,
        function() {
            ID('booking-filter').innerHTML = xhReq.responseText;
                  Booking.displayCalendar();
                  if (mode_value == 'calendar' && view_value == 'year') {
                      Booking.form.dview.value = 'month';
                  }

                  if (Booking.form['refresh-filter'] || !refresh_view) {
                      Booking.init();
                  } else {
                Booking.refresh(Booking.getCurrentURL());
            }
        }
    );



    return false;
}

/*
    Check if all required field are selected, then refresh calendar
*/
Booking.canRefresh = function() {

    var node = Booking.form.btype;

    if (node == 'select') {
        var btype = node.options[node.selectedIndex].value;
        var btypeRequired = node.parentNode.getElementsByTagName('span').length;
    } else {
        var btype = node.value;
        var btypeRequired = false;
    }

    var node = Booking.form.bcategory

    if (node == 'select') {
        var bcategory = node.options[node.selectedIndex].value;
          var bcategoryRequired = node.parentNode.getElementsByTagName('span').length;
    } else {
        var bcategory = node.value;
        var bcategoryRequired = false;
    }

    var node = Booking.form.bookableobject;

    if (node == 'select') {
          var bookableobject = node.options[node.selectedIndex].value;
          var bookableobjectRequired = node.parentNode.getElementsByTagName('span').length;
    } else {
        var bookableobject = node.value;
        var bookableobjectRequired = false;
    }

    if (bookableobject)
        Booking.form.bookableobject.value = bookableobject.split('|')[0];
    if ((!btype && btypeRequired)  ||
             (!bcategory && bcategoryRequired) || (!bookableobject && bookableobjectRequired)) {
        alert('veuillez remplir le(s) champs muni(s) d\'une balise rouge');
        return false;
    }

    Booking.refresh(Booking.getCurrentURL());
    return false;
}

Booking.onCalendarSelect = function(cal) {
    var timestamp = cal.date.getTime()/1000;
    Booking.form.ts.value = timestamp;

    if (!Booking.form['refresh-filter'])
        Booking.refresh(Booking.getCurrentURL());
}

function getPosition(node) {
    var x = 0; var y = 0;
    while (node.offsetParent) {
        x += node.offsetLeft;
        y += node.offsetTop;
        node = node.offsetParent;
    }
    return [ x, y ];
}

function centerContent(content) {
    var hh = window.innerHeight || document.documentElement.clientHeight;
    var ww = window.innerWidth || document.documentElement.clientWidth;
    var vscroll = document.documentElement.scrollTop || document.body.scrollTop;
    var hscroll = document.documentElement.scrollLeft || document.body.scrollLeft;
    if (content.offsetHeight > hh) {
        if (content.offsetTop != 50)
            window.scrollTo(0, 0);
        content.style.top = 50 + 'px';
    } else
        content.style.top  = (vscroll + (hh / 2) - (content.offsetHeight / 2))  + "px";

    content.style.left = (hscroll + (ww / 2) - (content.offsetWidth / 2)) + "px";
    window.onscroll = window.onresize = function() { centerContent(content); };
}

var BookingExport = {}
BookingExport.form = null;
BookingExport.startCalendar = null;
BookingExport.endCalendar = null;

BookingExport.init = function() {
    BookingExport.form = ID('booking-export-form');
    if (!BookingExport.form) {
        return false;
    }

    BookingExport.startCalendar = BookingExport.initCal('export-start-calendar', BookingExport.onStartSelect);
    BookingExport.endCalendar = BookingExport.initCal('export-end-calendar', BookingExport.onEndSelect);
    BookingExport.onStartSelect(BookingExport.startCalendar)
    BookingExport.onEndSelect(BookingExport.endCalendar)
}

BookingExport.initCal = function(containerId, callback) {
    var container = document.getElementById(containerId);
    var result = null;

    if (container && !container.childNodes.length) {
        var timestamp = new Date().getTime()
        result = new Calendar(1, timestamp, callback);
        result.create(container);
        result.show();
    }

    return result;
}

BookingExport.onStartSelect = function(cal) {
    var timestamp = cal.date.getTime();
    BookingExport.form.ts_start.value = parseInt(timestamp / 1000);
    if (timestamp > BookingExport.endCalendar.date.getTime()) {
        BookingExport.endCalendar.setDate(new Date(timestamp));
    }

}

BookingExport.onEndSelect = function(cal) {
    var timestamp = cal.date.getTime();
    BookingExport.form.ts_end.value = parseInt(timestamp / 1000);
    if (timestamp < BookingExport.startCalendar.date.getTime()) {
        BookingExport.startCalendar.setDate(new Date(timestamp));
    }
}

jQuery(document).ready(Booking.init);
jQuery(document).ready(Booking.showOnLoad);
jQuery(document).ready(BookingExport.init);