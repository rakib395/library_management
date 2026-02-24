

import { jsonrpc } from "@web/core/network/rpc_service";

document.addEventListener('DOMContentLoaded', function () {

    const searchInput = document.querySelector('input[name="search"]');
    
    if (!searchInput) return;

    const dropdown = document.createElement('div');
    dropdown.className = 'list-group shadow-lg position-absolute w-100 mt-1';
    dropdown.style.zIndex = '1000';
    searchInput.parentNode.appendChild(dropdown);


    searchInput.addEventListener('input', function () {

        const val = this.value;
        dropdown.innerHTML = '';

        if (val.length < 2) return;

        jsonrpc('/library/search/autocomplete', {
            term: val,
        }).then(function (data) {

            if (data.length > 0) {
                data.forEach(book => {
                    const item = document.createElement('a');
                    item.className = 'list-group-item list-group-item-action py-2';
                    item.href = '/library/book/' + book.id;
                    item.innerHTML = `<strong>${book.name}</strong> <br/><small class="text-muted">${book.author}</small>`;
                    dropdown.appendChild(item);
                });
            }

        });

    });


    document.addEventListener('click', function (e) {
        if (!searchInput.contains(e.target)) {
            dropdown.innerHTML = '';
        }
    });

});