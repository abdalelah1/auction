/* -------------------------------------------------------------------------------- /
	
	Magentech jQuery
	Created by Magentech
	v1.0 - 20.9.2016
	All rights reserved.

	+----------------------------------------------------+
		TABLE OF CONTENTS
	+----------------------------------------------------+
	[1]		Home page 5
	[2]		Home page 6
	[3]		Home page 8
	
/ -------------------------------------------------------------------------------- */

/* ---------------------------------------------------
	1.Home page 1
-------------------------------------------------- */

/* ---------------------------------------------------
	Listing Tabs - Slider
-------------------------------------------------- */




/* ---------------------------------------------------
	Owl carousel - Slider
-------------------------------------------------- */
$(document).ready(function ($) {
	"use strict";
	// Content slider
	$('.yt-content-slider').each(function () {
		var $slider = $(this),
			$panels = $slider.children('div'),
			data = $slider.data();
		// Remove unwanted br's
		//$slider.children(':not(.yt-content-slide)').remove();
		// Apply Owl Carousel
		
		$slider.owlCarousel2({
			responsiveClass: true,
			mouseDrag: true,
			video:true,
    		lazyLoad: (data.lazyload == 'yes') ? true : false,
			autoplay: (data.autoplay == 'yes') ? true : false,
			autoHeight: (data.autoheight == 'yes') ? true : false,
			autoplayTimeout: data.delay * 1000,
			smartSpeed: data.speed * 1000,
			autoplayHoverPause: (data.hoverpause == 'yes') ? true : false,
			center: (data.center == 'yes') ? true : false,
			loop: (data.loop == 'yes') ? true : false,
            dots: (data.pagination == 'yes') ? true : false,
            nav: (data.arrows == 'yes') ? true : false,
			dotClass: "owl2-dot",
			dotsClass: "owl2-dots",
            margin: data.margin,
            navText: ['',''],
			
			responsive: {
				0: {
					items: data.items_column4 
					},
				480: {
					items: data.items_column3
					},
				768: {
					items: data.items_column2
					},
				992: { 
					items: data.items_column1
					},
				1200: {
					items: data.items_column0 
					}
			}
		});
		
	});
	
	/*function buttonpage(element){
		var $element = $(element),
			$slider = $(".yt-content-slider", $element),
			data = $slider.data();
		if (data.buttonpage == "top") {
			$(".owl2-controls",$element).insertBefore($slider);
			$(".owl2-dots",$element).insertAfter($(".owl2-prev", $slider));
		} else {
			$(".owl2-nav",$element).insertBefore($slider);
			$(".owl2-controls",$element).insertAfter($slider);
		}	
	}
	
	// Home 1 - Latest Blogs
	(function (element) {
		buttonpage(element);
	})(".blog-sidebar");
	
	(function (element) {
		buttonpage(element);
	})("#so_extra_slider_1");
	
	(function (element) {
		buttonpage(element);
	})("#so_extra_slider_2");*/

}); 


// click header search header 
$(document).ready(function($) {
	$( ".search-header-w .icon-search" ).click(function() {
	$('#sosearchpro .search').slideToggle(200);
	$(this).toggleClass('active');
	});
});

/* ---------------------------------------------------
	1.Home page 5
-------------------------------------------------- */

/* ---------------------------------------------------
	2.Home page 6
-------------------------------------------------- */


//BLOCK Newsleter Popup
$(document).ready(function($) {
	$(window).load(function () {
		$('.common-home').addClass('hidden-scorll');
		$('.so_newletter_custom_popup_bg').addClass('popup_bg');
		$('input[name=\'hidden-popup\']').on('change', function(){
			if ($(this).is(':checked')) {
				checkCookie();
			} else {
				unsetCookie("so_newletter_custom_popup");
			}
		});
		function unsetCookie( name ) {
			document.cookie = name + '=; expires=Thu, 01 Jan 1970 00:00:01 GMT;';
		}
		$('.popup-close').click(function(){
			var this_close = $('.popup-close');
			this_close.parents().find('.common-home').removeClass('hidden-scorll');
			this_close.parents().find('#container-module-newletter').remove();
		});
	});
});

function setCookie(cname, cvalue, exdays) {
	var d = new Date();
	console.log(d.getTime());
	d.setTime(d.getTime() + (exdays*24*60*60*1000));
	var expires = "expires="+d.toUTCString();
	document.cookie = cname + "=" + cvalue + "; " + expires;
}
function getCookie(cname) {
	var name = cname + "=";
	var ca = document.cookie.split(';');
	for(var i=0; i<ca.length; i++) {
		var c = ca[i];
		while (c.charAt(0)==' ') c = c.substring(1);
		if (c.indexOf(name) == 0) return c.substring(name.length, c.length);
	}
	return "";
}
function checkCookie() {
	var check_cookie = getCookie("so_newletter_custom_popup");
	if(check_cookie == ""){
		setCookie("so_newletter_custom_popup", "Newletter Popup", 1 );
	}
}
function subscribe_newsletter()
{
	var emailpattern = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;
	var email = $('#txtemail').val();
	var d = new Date();
	var createdate = d.getFullYear() + '-' + (d.getMonth()+1) + '-' + d.getDate() + ' ' + d.getHours() + ':' + d.getMinutes() + ':' + d.getSeconds();
	var status   = 0;
	var dataString = 'email='+email+'&createdate='+createdate+'&status='+status;
	if(email != "")
	{
		if(!emailpattern.test(email))
		{
			$('.show-error').remove();
			$('.send-mail').after('<span class="show-error" style="color: red;margin-left: 10px"> Invalid Email </span>')
			return false;
		}
		else
		{
			$.ajax({
				url: 'index.php?route=extension/module/so_newletter_custom_popup/newsletter',
				type: 'post',
				data: dataString,
				dataType: 'json',
				success: function(json) {
					$('.show-error').remove();
					if(json.message == "Subscription Successfull") {
						checkCookie();
						$('.send-mail').after('<span class="show-error" style="color: #003bb3;margin-left: 10px"> ' + json.message + '</span>');
						setTimeout(function () {
							var this_close = $('.popup-close');
							this_close.parent().css('display', 'none');
							this_close.parents().find('.so_newletter_custom_popup_bg').removeClass('popup_bg');
						}, 3000);

					}else{
						$('.send-mail').after('<span class="show-error" style="color: red;margin-left: 10px"> ' + json.message + '</span>');
					}
					document.getElementById('signup').reset();
				}
			});
			return false;
		}
	}
	else
	{
		alert("Email Is Require");
		$(email).focus();
		return false;
	}
}

