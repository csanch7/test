const csrftoken = getCookie('csrftoken');
document.addEventListener('DOMContentLoaded', function() {
    
    document.addEventListener('click', event => {
        const element = event.target;
        if (element.className === 'edit btn') {
            edit(element.dataset.id)


        }
    })

})


function edit(postId) {
  fetch(`/edit/${postId}`, {
    method: 'PUT',
    headers: {'X-CSRFToken': csrftoken},
    mode: 'same-origin',
    body: JSON.stringify({ postcontent: document.querySelector('#edit-postcontent').value })
  })
  .then(response => response.json())
    .then(() => {
          window.location.assign("http://127.0.0.1:8000/")
        })

}
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