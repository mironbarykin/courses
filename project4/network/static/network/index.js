CURRENT_PAGE = 0
CONTENT_LOADED = 0

document.addEventListener('DOMContentLoaded', function() {
    // Post related events listeners.

    document.querySelector('#allposts-nav-button').addEventListener('click', function() {
        document.querySelector('#posts-view-follow').id = 'posts-view-all'
    });
    if (document.getElementById('following-nav-button') != null && typeof(document.getElementById('following-nav-button')) != 'undefined') {
        document.querySelector('#following-nav-button').addEventListener('click',  function() {
            console.log(document.querySelector('#posts-view-all'))
            CONTENT_LOADED++
            document.querySelector('#posts-view-all').id = 'posts-view-follow'
            document.querySelector('#posts-view-follow').innerHTML = ''
            load_posts('follow')
        });
    }

    if (document.getElementById('create-post-button') != null && typeof(document.getElementById('create-post-button')) != 'undefined') {
        document.querySelector('#create-post-button').addEventListener('click', add_post);
    }
    if (document.getElementById('follow-button') != null && typeof(document.getElementById('follow-button')) != 'undefined') {
        document.querySelector('#follow-button').addEventListener('click', follow_user);
    }

    if (document.getElementById('posts-view-all') != null && typeof(document.getElementById('posts-view-all')) != 'undefined' && CONTENT_LOADED == 0) {
        CONTENT_LOADED++
        document.querySelector('#posts-view-all').innerHTML = ''
        load_posts('allposts')
    } else if (document.getElementById('posts-view-profile') != null && typeof(document.getElementById('posts-view-all')) != 'undefined' && CONTENT_LOADED == 0) {
        CONTENT_LOADED++
        load_posts(document.querySelector('.username-data').id)
    }
    // Loading userpage after button have clicked. DONT NEED 
    // document.querySelector('#userpage-nav-button').addEventListener('click');
})

function add_post(){
    fetch('/post', { method: 'POST', body: JSON.stringify({ content: document.querySelector('#create-post-content').value }) })
    .then(response => response.json())
    .then(result => {
        alert(result.message);
    });
}


function follow_user(){
    let action
    if (document.querySelector('#follow-button').innerHTML == 'Follow!') {
        action = 'follow'
    } else if (document.querySelector('#follow-button').innerHTML == 'Unfollow!') {
        action = 'unfollow'
    }
    
    fetch(`/user/${action}`, { method: 'POST', body: JSON.stringify({ profile: document.querySelector('.username-data').id }) })
    .then(response => response.json())
    .then(result => {
        alert(result.message);
        location.reload()
    });
    
}


function paginator_button_check(posts_length){
    if (CURRENT_PAGE > 0){ document.querySelector("#paginator-previous").parentElement.classList.remove("disabled") } else { document.querySelector("#paginator-previous").parentElement.classList.add("disabled") }
    if (CURRENT_PAGE >= posts_length - 1){ document.querySelector("#paginator-next").parentElement.classList.add("disabled") } else { document.querySelector("#paginator-next").parentElement.classList.remove("disabled") }
}


function load_posts(type){
    fetch(`posts/${type}`)
    .then(response => response.json())
    .then(posts => {
        document.querySelector("#paginator-previous").addEventListener('click', function(){
            CURRENT_PAGE -= 1
            if (document.getElementById('posts-view-all') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
                document.querySelector('#posts-view-all').innerHTML = ''
            } else if (document.getElementById('posts-view-follow') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
                document.querySelector('#posts-view-follow').innerHTML = ''
            } else if (document.getElementById('posts-view-profile') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
                document.querySelector('#posts-view-profile').innerHTML = ''
            }
            posts[CURRENT_PAGE].forEach(load_post)
            paginator_button_check(posts.length)
        })
        document.querySelector("#paginator-next").addEventListener('click', function(){
            CURRENT_PAGE += 1
            if (document.getElementById('posts-view-all') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
                document.querySelector('#posts-view-all').innerHTML = ''
            } else if (document.getElementById('posts-view-follow') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
                document.querySelector('#posts-view-follow').innerHTML = ''
            } else if (document.getElementById('posts-view-profile') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
                document.querySelector('#posts-view-profile').innerHTML = ''
            }
            posts[CURRENT_PAGE].forEach(load_post)
            paginator_button_check(posts.length)
        })
        // Loading each post for the first time
        posts[CURRENT_PAGE].forEach(load_post)
    })
}


function load_post(contents){
    // Creating div element for post
    const post = document.createElement('div');
        post.className = 'post';
        // Adding in div content, author (with link), timestamp (in python modified), and image for liking.
        post.innerHTML = `<span id="post-content${contents.id}">${contents.content}</span><br> <a class="post-author" href="profile/${contents.author.id}">${contents.author.username}</a> at ${contents.timestamp} <b id="post-count${contents.id}">${contents.likes.users.length}</b><img class="post-like" id="post-like${contents.id}" src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Heart_coraz%C3%B3n.svg/2048px-Heart_coraz%C3%B3n.svg.png">`;
        // Creating button for post edit
        if (contents.author.id == contents.userid){
            const editbutton = document.createElement('button');
            editbutton.className = 'btn btn-primary'
            editbutton.id = `post-edit${contents.id}`
            editbutton.innerHTML = 'Edit'
            editbutton.style = 'height: 28px; padding: 0rem .75rem'
            post.append(editbutton);
        }
        if (document.getElementById('posts-view-all') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
            document.querySelector('#posts-view-all').append(post)
        } else if (document.getElementById('posts-view-follow') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
            document.querySelector('#posts-view-follow').append(post)
        } else if (document.getElementById('posts-view-profile') != null && typeof(document.getElementById('posts-view-all')) != 'undefined') {
            document.querySelector('#posts-view-profile').append(post)
        }
    // Adding event listener for checking edit button clicks
    if (contents.author.id == contents.userid){
        document.querySelector(`#post-edit${contents.id}`).addEventListener('click', function(){
            if (document.querySelector(`#post-edit${contents.id}`).innerHTML == 'Edit'){
                const editfield = document.createElement('textarea')
                editfield.id = `post-editing${contents.id}`
                editfield.value = contents.content
                document.querySelector(`#post-content${contents.id}`).innerHTML = ''
                document.querySelector(`#post-content${contents.id}`).append(editfield)
                document.querySelector(`#post-edit${contents.id}`).innerHTML = 'Save'
            } else if (document.querySelector(`#post-edit${contents.id}`).innerHTML == 'Save') {
                fetch(`/post/${contents.id}`, { method: 'PUT', body: JSON.stringify({ type: 'editing', content: document.querySelector(`#post-editing${contents.id}`).value }) })
                .then(response => response.json())
                .then(result => {
                    document.querySelector(`#post-content${contents.id}`).removeChild(document.querySelector(`#post-editing${contents.id}`))
                    document.querySelector(`#post-content${contents.id}`).innerHTML = result.content
                })
                document.querySelector(`#post-edit${contents.id}`).innerHTML = 'Edit'
            }
        })
    }
    // Checking if user is already put a like on the post
    if (contents.likes.users.includes(contents.userid)){ document.querySelector(`#post-like${contents.id}`).style.filter = 'brightness(1)' } else { document.querySelector(`#post-like${contents.id}`).style.filter = 'brightness(0)' }
    // Adding event listener for LIKE button.
    document.querySelector(`#post-like${contents.id}`).addEventListener('click', function() {
        if (document.querySelector(`#post-like${contents.id}`).style.filter == 'brightness(1)'){
            fetch(`/post/${contents.id}`, { method: 'PUT', body: JSON.stringify({ type: 'liking', liked: false }) })
            document.querySelector(`#post-count${contents.id}`).innerHTML = contents.likes.users.length -= 1
            document.querySelector(`#post-like${contents.id}`).style.filter = 'brightness(0)'
        } else if (document.querySelector(`#post-like${contents.id}`).style.filter == 'brightness(0)'){
            fetch(`/post/${contents.id}`, { method: 'PUT', body: JSON.stringify({ type: 'liking', liked: true }) })
            document.querySelector(`#post-count${contents.id}`).innerHTML = contents.likes.users.length += 1
            document.querySelector(`#post-like${contents.id}`).style.filter = 'brightness(1)'
        }
    })
}

