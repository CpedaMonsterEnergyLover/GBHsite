let card_title;
$('.equipment-card').hover(function() {
    let a = Math.random() * 6 - 3;
    $(this).css('transform', 'rotate(' + a + 'deg) scale(1.4)');
    $(this).css('z-index', '100');
    card_title = $(this).find('.equipment-card-text-name').text()
    $(this).find('.equipment-card-text-name').text($(this).find('.equipment-card-text-description').text())
}, function() {
    $(this).css('transform', 'none');
    $(this).css('z-index', '10');
    $(this).find('.equipment-card-text-name').text(card_title)
})
