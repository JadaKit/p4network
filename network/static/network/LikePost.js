document.addEventListener('DOMContentLoaded', function () {
    let likeButtons = document.querySelectorAll('.postLikeBtn');

    likeButtons.forEach(button => {
        button.addEventListener('click', function () {
            let post_id = this.dataset.postId;
            let postLikeBtn = this;
            let postLikeCounter = this.querySelector('.likeCount');

            fetch('/like_post/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({
                    post_id: post_id
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    if (postLikeCounter) {
                        postLikeCounter.textContent = data.like_count;
                    }

                    if (data.liked) {
                        postLikeBtn.classList.add('active');
                    } else {
                        postLikeBtn.classList.remove('active');
                    }
                } else {
                    console.error('Error liking post:', data.message);
                }
            })
            .catch(error => {
                console.error('Error:', error);
            });
        });
    });
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
