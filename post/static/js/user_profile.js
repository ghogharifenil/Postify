document.querySelectorAll(".save-btn").forEach((btn) => {
  btn.addEventListener("click", function () {
    let postId = this.dataset.id;

    fetch(`/save_post/${postId}/`)
      .then((response) => response.json())
      .then((data) => {
        if (data.saved) {
          this.innerHTML =
            '<i class="fa-solid fa-bookmark"></i><span>Unsave</span>';
        } else {
          this.innerHTML =
            '<i class="fa-regular fa-bookmark"></i><span>Save</span>';
        }
      });
  });
});

document.querySelectorAll(".like-btn").forEach((btn) => {
  btn.addEventListener("click", function (e) {
    e.stopPropagation();

    let postId = this.dataset.id;

    fetch(`/like/${postId}/`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Request failed");
        }
        return response.json();
      })
      .then((data) => {
        this.innerHTML = data.liked
          ? `<i class="fa-solid fa-heart" style="color:red;"></i><span>${data.total_likes}</span>`
          : `<i class="fa-regular fa-heart"></i><span>${data.total_likes}</span>`;
      })
      .catch((err) => {
        console.log(err);
      });
  });
});

function toggleMenu(event, button) {
  event.stopPropagation();

  document.querySelectorAll(".menu-dropdown").forEach((menu) => {
    if (menu !== button.nextElementSibling) {
      menu.style.display = "none";
    }
  });

  const menu = button.nextElementSibling;

  menu.style.display = menu.style.display === "block" ? "none" : "block";
}

document.addEventListener("click", function () {
  document.querySelectorAll(".menu-dropdown").forEach((menu) => {
    menu.style.display = "none";
  });
});
function showLikes(event, postId) {
  event.preventDefault();
  event.stopPropagation();

  fetch(`/like_users/${postId}/`)
    .then((response) => response.json())
    .then((data) => {
      let html = "";

      if (data.likes.length === 0) {
        html = `
                    <div style="padding:25px;text-align:center;color:#aaa;">
                        No Likes Yet ❤️
                    </div>
                `;
      } else {
        data.likes.forEach((user) => {
          html += `
 <a href="/user-profile/${user.id}/" class="like-user">

    ${
      user.profile_pic
        ? `<img src="${user.profile_pic}" class="like-avatar">`
        : `<div class="like-avatar no-avatar">
                ${user.name.charAt(0).toUpperCase()}
           </div>`
    }

    <span>${user.name}</span>

</a>
`;
        });
      }

      document.getElementById("likesList").innerHTML = html;
      document.getElementById("likesPopup").style.display = "flex";
    })
    .catch((error) => {
      console.log(error);
    });
}

function closeLikes() {
  document.getElementById("likesPopup").style.display = "none";
}

// Popup બહાર click થાય તો close
document.getElementById("likesPopup").addEventListener("click", function (e) {
  if (e.target === this) {
    closeLikes();
  }
});

// ESC key થી close
document.addEventListener("keydown", function (e) {
  if (e.key === "Escape") {
    closeLikes();
  }
});
