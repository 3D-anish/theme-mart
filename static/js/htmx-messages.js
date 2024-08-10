;(function () {
    const toastOptions = { delay: 2000 }
  
    function createToast(message) {
        $.notify({
            icon: '',
            title: '',
            message: `${message.message}`
          }, {
            element: 'body',
            position: null,
            type: `${message.tags}`,
            allow_dismiss: true,
            newest_on_top: true,
            showProgressbar: true,
            placement: {
              from: "top",
              align: "right"
            },
            offset: 20,
            spacing: 10,
            z_index: 1031,
            delay: 5000,
            animate: {
              enter: 'animated fadeInDown',
              exit: 'animated fadeOutUp'
            },
            icon_type: 'class',
            template: '<div data-notify="container" class="col-xs-11 col-sm-3 alert alert-{0}" role="alert">' +
              '<button type="button" aria-hidden="true" class="btn-close" data-notify="dismiss"></button>' +
              '<span data-notify="icon"></span> ' +
              '<span data-notify="title"> {1} </span> ' +
              '<span data-notify="message"> {2}</span>' +
              '<div class="progress" data-notify="progressbar">' +
              '<div class="progress-bar progress-bar-{0}" role="progressbar" aria-valuenow="0" aria-valuemin="0" aria-valuemax="100" style="width: 0%;"></div>' +
              '</div>' +
              '<a href="{3}" target="{4}" data-notify="url"></a>' +
              '</div>'
          });
    }
  
    htmx.on("messages", (event) => {
      event.detail.value.forEach(createToast)
    })
  
    // Show all existsing toasts, except the template
    htmx.findAll(".toast:not([data-toast-template])").forEach((element) => {
      const toast = new bootstrap.Toast(element, toastOptions)
      toast.show()
    })
  })()