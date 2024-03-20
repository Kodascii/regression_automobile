$(document).ready(function() {
    $('.categoryButton').on('click', function() {
        const targetCategory = $(this).data('target-category');
        $('.category').hide();
        $('.' + targetCategory).show();
        $('.itemButtons').hide();
        $('.' + targetCategory + 'Buttons').show();
        showFirstItem($('.' + targetCategory));
    });

    $('.itemButton').on('click', function() {
        const itemName = $(this).data('target-item');
        $('.categoryItem').each(function() {
            if ($(this).data('item-name') === itemName) {
                $(this).show();
            } else {
                $(this).hide();
            }
        });
    });

    // Show the first category and its items by default
    $('.categoryButton[data-target-category="byprice"]').click();
});

function showFirstItem(category) {
    category.find('.categoryItem').hide().first().show();
}