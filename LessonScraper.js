// JavaScript source code

// gets list of all swiss german phrases
// TODO get translations, pair them
//[...document.querySelectorAll('b.sc-hHOBVR.jnovYm')].map(elm => elm.innerHTML.trim().replace(/[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~…]/g, "")).filter(a => a != "")

//Does it!!!!
// TODO seperate sentences on same line using puncuation like
// What color do you want? Blue maybe?
// into "What color do you want?" "Blue maybe?"
[...document.querySelectorAll('b.sc-hHOBVR.jnovYm')].filter(elm => elm.innerHTML.trim() != '').map(elm => [elm.innerHTML.trim().replace(/[!"#$%&()*+,-./:;<=>?@[\]^_`{|}~]/g, ""), (elm.nextSibling.data || '').trim()])