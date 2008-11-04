/*
* Utilities for the Upload Reference Widget
*/

function addUploadReferenceInput(field) {
    var place = document.getElementById(field + '_inputs');
    var br = document.createElement('br');
    place.appendChild(br);
    var input = document.createElement('input');
    input.size = '30';
    input.type = 'file';
    input.name = field + '_file:list';
    place.appendChild(input);
    return false;
}

function showUploadReference(field) {
    document.getElementById('box_' + field + '_select').style.display = 'none';
    document.getElementById('box_' + field + '_upload').style.display = 'block';
}

function hideUploadReference(field) {
    document.getElementById('box_' + field + '_upload').style.display = 'none';
    document.getElementById('box_' + field + '_select').style.display = 'block';
}
