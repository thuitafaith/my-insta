// $(document).ready(function(){
//
//   $('.fa-heart').each(function(e) {
//   $(this).click(function(e) {
//     e.preventDefault()
//
//     var $this = $(this)
//     var like_status
//
//     if ($this.attr("class") == ('fas fa-heart' || 'fa-heart fas')) {
//       like_status = true
//     }
//     if ($this.attr("class") == ('far fa-heart' || 'fa-heart far')) {
//       like_status = false
//     }
//
//     $.ajax({
//       type: "POST",
//       url: $(this).attr("data-href"),
//       data: {
//         like: like_status
//       },
//       success: function(resp) {
//         if (resp == 'liked') {
//           $this.removeClass('far')
//           $this.addClass('fas');
//           location.reload();
//         }
//         if (resp == 'unliked') {
//           $this.removeClass('fas')
//           $this.addClass('far');
//           location.reload();
//         }
//       }
//     })
//   })
// })
// })
