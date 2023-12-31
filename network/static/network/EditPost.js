function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function editPost(postId) {
    document.getElementById(`postContent_${postId}`).style.display = 'none';
    document.getElementById(`editTextArea_${postId}`).style.display = 'block';
    document.querySelector(`.editPostBtn`).style.display = 'none';
    document.querySelector(`.savePostBtn`).style.display = 'block';
}

function savePost(postId) {
    const content = document.getElementById(`editTextArea_${postId}`).value;

    const csrfToken = getCookie('csrftoken');

    fetch('/edit_post/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            post_id: postId,
            content: content,
        }),
    })
    .then(response => response.json())
    .then(data => {
        // Обработка успешного сохранения, например, обновление интерфейса
        console.log(data);
        document.getElementById(`postContent_${postId}`).innerText = content;
        document.getElementById(`postContent_${postId}`).style.display = 'block';
        document.getElementById(`editTextArea_${postId}`).style.display = 'none';
        document.querySelector(`.editPostBtn`).style.display = 'block';
        document.querySelector(`.savePostBtn`).style.display = 'none';
    })
    .catch(error => console.error('Error:', error));
}
