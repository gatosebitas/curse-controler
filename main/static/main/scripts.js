var $useAccountBtn = $('#use-account-btn')
var $useAccountBtnState = getBtnState($useAccountBtn);
var $endSessionBtn = $('#end-session-btn')
var $endSessionBtnState = getBtnState($endSessionBtn);

enableBtn($endSessionBtn, $endSessionBtnState);
enableBtn($useAccountBtn, $useAccountBtnState);

$endSessionBtn.click(function(){
    disableBtn($endSessionBtn);
    $.ajax({url: `/sessions/${sessionId}/`, type: 'PUT'})
        .done(function(resp){
            window.location.reload();
        })
        .fail(function(err){
            if (err.status === 400) {
                alert(err.responseText);
            }
            enableBtn($endSessionBtn, $endSessionBtnState);
        })
});

$('#main-form').submit(function(ev){
    ev.preventDefault();
    disableBtn($useAccountBtn);
    $.post('/sessions/',{
            session_time: parseInt($('#session-time').val()),
            personEmail: personEmail
        })
        .done(function(resp){
            window.location.reload();
        })
        .fail(function(err){
            if (err.status === 400) {
                alert(err.responseText)
                window.location.reload();
            }
        })
        .always(function(){
            enableBtn($useAccountBtn, $useAccountBtnState);
        });
});

function statusHandler(resp) {
   if (resp.status === 'connected') {
        if (!isAuthenticated) {
            getUserFromFacebook();
        }
        console.log('connected')
    } else {
        if (isAuthenticated) {
            console.log('no connected')
            endSesionOnServer();
        }
    }
}
function onLoggedIn() {
    $('#no-session-message').html('Espere por favor...');
    FB.getLoginStatus(function(resp) {
        if (resp.status === 'connected') {
            getUserFromFacebook();
        } else {
           endSesionOnServer();
        }
    });
}

function startSesionOnServer(payload) {
    $.post('/login/', payload).done(function(data){
        window.location.reload();
        console.log('data:', data)
    }).fail(function(err){
        console.log('err:', err)
    });
}
function endSesionOnServer() {
    $.post('/logout/').done(function(data){
        window.location.reload();
        console.log('data:', data)
    }).fail(function(err){
        console.log('err:', err)
    });
}

function disableBtn(btn, action) {
    btn.prop('disabled', true);
    btn.html(action || 'Espere por favor...');
    btn.css('background', 'gray');
    btn.css('color', '#fff');
}

function enableBtn(btn, state) {
    btn.prop('disabled', false);
    btn.html(state.html);
    btn.css('background', state.background);
    btn.css('color', state.color);
}

function getBtnState(btn) {
    return {
        color: btn.css('color'),
        background: btn.css('background'),
        html: btn.html()
    }
}
function trackRemaining(remaining){
    setInterval(function(){
        console.log('remaining:', remaining)
        if (remaining === 0){
            window.location.reload();
        }
        remaining -= 1;
    }, 1000);
}

function getUserFromFacebook() {
    FB.api('/me', {fields: 'name,email,first_name,last_name,picture'},function(data) {
        data.picture = data.picture.data.url;
        startSesionOnServer(data);
    });
}