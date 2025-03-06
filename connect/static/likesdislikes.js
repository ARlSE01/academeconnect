document.addEventListener("DOMContentLoaded", function () {
    function setupButtons(buttonClass, urlPattern) {
        document.querySelectorAll(buttonClass).forEach(button => {
            button.addEventListener("click", function () {
                let itemId = this.dataset.post;  // Works for both posts and comments
                let url = urlPattern.replace("ITEM_ID", itemId);

                fetch(url, { method: "POST", headers: { "X-CSRFToken": getCSRFToken() } })
                    .then(response => response.json())
                    .then(data => {
                        document.querySelector(`#likes-count-${itemId}`).innerText = data.likes;
                        document.querySelector(`#dislikes-count-${itemId}`).innerText = data.dislikes;
                    });
            });
        });
    }

    setupButtons(".like-btn", "/like/post/ITEM_ID/");
    setupButtons(".dislike-btn", "/dislike/post/ITEM_ID/");
    setupButtons(".comment-like-btn", "/like/comment/ITEM_ID/");
    setupButtons(".comment-dislike-btn", "/dislike/comment/ITEM_ID/");

    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});