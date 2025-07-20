document.addEventListener('DOMContentLoaded', function() {
    const csrftoken = getCookie('csrftoken');
    let user = document.querySelector(`.follow`).dataset.id
    
    const followBtn = document.querySelector(`.follow`);
    const unfollowBtn = document.querySelector(`.unfollow`);
    const state = localStorage.getItem(`followState-${user}`);
    if (state === 'false') {
            followBtn.style.display = 'none';
            unfollowBtn.style.display = 'block';
        } else {
            followBtn.style.display = 'block';
            unfollowBtn.style.display = 'none';
        }

    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'follow') {
            fetch(`/follow/${document.querySelector('#username').innerHTML}`, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            body: JSON.stringify({ following: true })
            })
            .then(() => {
                
                localStorage.setItem(`followState-${user}`, 'false');
                window.location.href = `/user/${document.querySelector('#username').innerHTML}`;
            })
            
        }
        if (element.className === 'unfollow') {
            fetch(`/follow/${document.querySelector('#username').innerHTML}`, {
            method: 'PUT',
            headers: {'X-CSRFToken': csrftoken},
            mode: 'same-origin',
            body: JSON.stringify({ following: false })
            })
            .then(() => {
                
                localStorage.setItem(`followState-${user}`, 'true');
                window.location.href = `/user/${document.querySelector('#username').innerHTML}`;
            })
        }
    })
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
})

