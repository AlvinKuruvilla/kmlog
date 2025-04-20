// Elements
const toggleThemeBtn = document.querySelector('.header__theme-button');
const storiesContent = document.querySelector('.stories__content');
const storiesLeftButton = document.querySelector('.stories__left-button');
const storiesRightButton = document.querySelector('.stories__right-button');
const posts = document.querySelectorAll('.post');
const postsContent = document.querySelectorAll('.post__content');

// ===================================
// DARK/LIGHT THEME
// Set initial theme from LocalStorage
document.onload = setInitialTheme(localStorage.getItem('theme'));
function setInitialTheme(themeKey) {
  if (themeKey === 'dark') {
    document.documentElement.classList.add('darkTheme');
  } else {
    document.documentElement.classList.remove('darkTheme');
  }
}

// Toggle theme button
toggleThemeBtn.addEventListener('click', () => {
  // Toggle root class
  document.documentElement.classList.toggle('darkTheme');

  // Saving current theme on LocalStorage
  if (document.documentElement.classList.contains('darkTheme')) {
    localStorage.setItem('theme', 'dark');
  } else {
    localStorage.setItem('theme', 'light');
  }
});

// ===================================
// STORIES SCROLL BUTTONS
// Scrolling stories content
storiesLeftButton.addEventListener('click', () => {
  storiesContent.scrollLeft -= 320;
});
storiesRightButton.addEventListener('click', () => {
  storiesContent.scrollLeft += 320;
});

// Checking if screen has minimun size of 1024px
if (window.matchMedia('(min-width: 1024px)').matches) {
  // Observer to hide buttons when necessary
  const storiesObserver = new IntersectionObserver(
    function (entries) {
      entries.forEach((entry) => {
        if (entry.target === document.querySelector('.story:first-child')) {
          storiesLeftButton.style.display = entry.isIntersecting
            ? 'none'
            : 'unset';
        } else if (
          entry.target === document.querySelector('.story:last-child')
        ) {
          storiesRightButton.style.display = entry.isIntersecting
            ? 'none'
            : 'unset';
        }
      });
    },
    { root: storiesContent, threshold: 1 }
  );

  // Calling the observer with the first and last stories
  storiesObserver.observe(document.querySelector('.story:first-child'));
  storiesObserver.observe(document.querySelector('.story:last-child'));
}

// ===================================
// POST MULTIPLE MEDIAS
// Creating scroll buttons and indicators when post has more than one media
posts.forEach((post) => {
  if (post.querySelectorAll('.post__media').length > 1) {
    const leftButtonElement = document.createElement('button');
    leftButtonElement.classList.add('post__left-button');
    leftButtonElement.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <path fill="#fff" d="M256 504C119 504 8 393 8 256S119 8 256 8s248 111 248 248-111 248-248 248zM142.1 273l135.5 135.5c9.4 9.4 24.6 9.4 33.9 0l17-17c9.4-9.4 9.4-24.6 0-33.9L226.9 256l101.6-101.6c9.4-9.4 9.4-24.6 0-33.9l-17-17c-9.4-9.4-24.6-9.4-33.9 0L142.1 239c-9.4 9.4-9.4 24.6 0 34z"></path>
      </svg>
    `;

    const rightButtonElement = document.createElement('button');
    rightButtonElement.classList.add('post__right-button');
    rightButtonElement.innerHTML = `
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">
        <path fill="#fff" d="M256 8c137 0 248 111 248 248S393 504 256 504 8 393 8 256 119 8 256 8zm113.9 231L234.4 103.5c-9.4-9.4-24.6-9.4-33.9 0l-17 17c-9.4 9.4-9.4 24.6 0 33.9L285.1 256 183.5 357.6c-9.4 9.4-9.4 24.6 0 33.9l17 17c9.4 9.4 24.6 9.4 33.9 0L369.9 273c9.4-9.4 9.4-24.6 0-34z"></path>
      </svg>
    `;

    post.querySelector('.post__content').appendChild(leftButtonElement);
    post.querySelector('.post__content').appendChild(rightButtonElement);

    post.querySelectorAll('.post__media').forEach(function () {
      const postMediaIndicatorElement = document.createElement('div');
      postMediaIndicatorElement.classList.add('post__indicator');

      post
        .querySelector('.post__indicators')
        .appendChild(postMediaIndicatorElement);
    });

    // Observer to change the actual media indicator
    const postMediasContainer = post.querySelector('.post__medias');
    const postMediaIndicators = post.querySelectorAll('.post__indicator');
    const postIndicatorObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            // Removing all the indicators
            postMediaIndicators.forEach((indicator) =>
              indicator.classList.remove('post__indicator--active')
            );
            // Adding the indicator that matches the current post media
            postMediaIndicators[
              Array.from(postMedias).indexOf(entry.target)
            ].classList.add('post__indicator--active');
          }
        });
      },
      { root: postMediasContainer, threshold: 0.5 }
    );

    // Calling the observer for every post media
    const postMedias = post.querySelectorAll('.post__media');
    postMedias.forEach((media) => {
      postIndicatorObserver.observe(media);
    });
  }
});

// Adding buttons features on every post with multiple medias
postsContent.forEach((post) => {
  if (post.querySelectorAll('.post__media').length > 1) {
    const leftButton = post.querySelector('.post__left-button');
    const rightButton = post.querySelector('.post__right-button');
    const postMediasContainer = post.querySelector('.post__medias');

    // Functions for left and right buttons
    leftButton.addEventListener('click', () => {
      postMediasContainer.scrollLeft -= 400;
    });
    rightButton.addEventListener('click', () => {
      postMediasContainer.scrollLeft += 400;
    });

    // Observer to hide button if necessary
    const postButtonObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach((entry) => {
          if (entry.target === post.querySelector('.post__media:first-child')) {
            leftButton.style.display = entry.isIntersecting ? 'none' : 'unset';
          } else if (
            entry.target === post.querySelector('.post__media:last-child')
          ) {
            rightButton.style.display = entry.isIntersecting ? 'none' : 'unset';
          }
        });
      },
      { root: postMediasContainer, threshold: 0.5 }
    );

    if (window.matchMedia('(min-width: 1024px)').matches) {
      postButtonObserver.observe(
        post.querySelector('.post__media:first-child')
      );
      postButtonObserver.observe(post.querySelector('.post__media:last-child'));
    }
  }
});
const commentButton = document.getElementById('comment_button');
const commentBox = document.getElementById('comment_box');
const postCommentButton = document.getElementById('post_comment');

// Show the comment box
postCommentButton.addEventListener('click', async () => {
  console.log('Comment Post button clicked!');
  try {
    const response = await fetch('http://127.0.0.1:5000/end-server', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
    });
    console.log(response);
    if (!response.ok) {
      const errorData = await response.json();
      alert('Failed to send special request:', errorData);
      return;
    }

    const result = await response.json();
    alert('Response from Python server:', result);
  } catch (error) {
    console.log('Error:', error);
  }

  if (commentBox.style.display === 'block') {
    commentBox.style.display = 'none'; // Hide the comment box
  } else {
    commentBox.style.display = 'block'; // Show the comment box
  }
});

// Hide the comment box and clear the textarea
postCommentButton.addEventListener('click', () => {
  commentBox.style.display = 'none';
  document.getElementById('comment_input').value = '';
});
function startKeyLogger(user_id_str, platform_initial, task_id) {
  const keyEvents = [];

  document.addEventListener('keydown', (e) =>
    keyEvents.push(['P', e.key, Date.now()])
  );
  document.addEventListener('keyup', (e) =>
    keyEvents.push(['R', e.key, Date.now()])
  );

  const button = document.createElement('button');
  button.textContent = 'Submit Keylog';
  button.style.position = 'fixed';
  button.style.bottom = '10px';
  button.style.right = '10px';
  button.style.background = 'black';
  button.style.color = 'white';
  document.body.appendChild(button);

  // --- click handler ---------------------------------------------------------
  button.onclick = async () => {
    /* 1 — build filename ----------------------------------------------------- */
    const platform_letter =
      platform_initial === '0'
        ? 'f'
        : platform_initial === '1'
        ? 'i'
        : platform_initial === '2'
        ? 't'
        : 'u'; // u = unknown / fallback
    const filename = `${platform_letter}_${user_id_str}_${task_id}.csv`;

    /* 2 — build CSV blob ----------------------------------------------------- */
    const heading = [['Press or Release', 'Key', 'Time']];
    const csvString = heading
      .concat(keyEvents)
      .map((row) => row.join(','))
      .join('\n');
    const blob = new Blob([csvString], {
      type: 'text/csv;charset=utf-8',
    });

    /* 3 — send to Netlify Function ------------------------------------------ */
    const formData = new FormData();
    formData.append('file', blob, filename); // filename → Content‑Disposition

    try {
      const res = await fetch(
        'https://melodious-squirrel-b0930c.netlify.app/.netlify/functions/saver',
        {
          method: 'POST',
          body: formData, // fetch sets the correct multipart boundary
        }
      );
      const result = await res.json();

      if (res.ok && result.url) {
        console.log('✅ Uploaded!', result.url);
        console.log(`✅ Uploaded!\nURL: ${result.url}`);
      } else {
        console.error('❌ Upload failed:', result);
      }
    } catch (err) {
      console.error('❌ Network/function error:', err);
      alert('❌ Could not reach serverless function');
    }
    const typed_text_blob = new Blob(
      [document.getElementById('comment_input').value],
      {
        type: 'text/plain;charset=utf-8',
      }
    );
    const typed_text_form_data = new FormData();
    const raw_text_filename = `${platform_letter}_${user_id_str}_${task_id}_raw.txt`;

    typed_text_form_data.append('file', typed_text_blob, raw_text_filename);
    try {
      const res = await fetch(
        'https://melodious-squirrel-b0930c.netlify.app/.netlify/functions/saver',
        {
          method: 'POST',
          body: typed_text_form_data, // fetch sets the correct multipart boundary
        }
      );
      const result = await res.json();

      if (res.ok && result.url) {
        console.log('✅ Uploaded!', result.url);
        console.log(`✅ Uploaded!\nURL: ${result.url}`);
      } else {
        console.error('❌ Upload failed:', result);
      }
    } catch (err) {
      console.error('❌ Network/function error:', err);
      alert('❌ Could not reach serverless function');
    }
  };
}

function getQueryParam(name) {
  return new URLSearchParams(window.location.search).get(name);
}

window.onload = async function () {
  const user_id = getQueryParam('user_id');
  const platform_id = getQueryParam('platform_id');
  const task_id = getQueryParam('task_id');

  if (user_id && platform_id && task_id) {
    startKeyLogger(user_id, platform_id, task_id);
  } else {
    alert('Missing user or platform or task info in URL');
  }
};
