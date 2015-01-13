/*
 * jQuery Typeahead Tagging v0.3
 *
 * A jQuery plugin to allow managing tags with typeahead autocompletion.
 *
 * Latest source at https://github.com/bitmazk/jquery-typeahead-tagging
 *
 * Current issues/TODOs/Next up features:
 * - first hit of ENTER must complete, the second (in the empty input) must submit
 * - prevent umlauts from being cleaned out
 * - implement option dict and different actions
 *   Options:
 *   - tagsource: array
 *   - typeahead: boolean
 *   - tag_limit: integer
 *   Actions:
 *   - value: with parameter > sets value / without parameter > returns the input value
 *   - tags: returns the list of tags. Not the input value, but the actual array of strings
 *   - destroy: removes the plugin, re-enables original input
 *
 * Feature wishlist:
 * - make it work without typeahead as standalone tagging plugin
 * - add a data-tags-url so that it is possible to initialize the plugin only via data attributes.
 *   the view must then return the list of tags
 * - add listener for when the input is updated, so that it is reflected in the tag input
 * - make the new tag input expand automatically when typing
 *
 */

// adding IE < 9 compatibility for indexOf. Taken from developer.mozilla.org
if (!Array.prototype.indexOf) {
    Array.prototype.indexOf = function (searchElement, fromIndex) {
        var k;
        if (this === null) {
            throw new TypeError('"this" is null or not defined');
        }
        var O = Object(this);
        var len = O.length >>> 0; // jshint ignore:line
        if (len === 0) {
            return -1;
        }
        var n = +fromIndex || 0;

        if (Math.abs(n) === Infinity) {
            n = 0;
        }
        if (n >= len) {
            return -1;
        }
        k = Math.max(n >= 0 ? n : len - Math.abs(n), 0);
        while (k < len) {
            if (k in O && O[k] === searchElement) {
                return k;
            }
            k++;
        }
        return -1;
    };
}


function TypeaheadTaggingPlugin(element) {

    this.element = element;                                             // the original input element
    this.input = undefined;                                             // the typeahead input
    this.ul = undefined;                                                // the ul that wraps around the tags
    this.cleaning_pattern = /[^\w\s-]+/g;                               // The regex pattern to clean tags with.
    this.typeahead_datasetname = 'tagging';                             // The name of the typeahead dataset.
    this.max_tags = parseInt(this.element.getAttribute('data-max-tags')) || 9001; // get the maximum tag count from the element or set it to over 9000

}

TypeaheadTaggingPlugin.prototype.add_tag = function (value, mute) {

    // adds the tag to the value and creates a new tag element

    value = this.clean_value(value);

    if (!value) {
        return
    }

    if (this.add_to_value(value)) {
        this.append_li(value);
    }

    jQuery(this.input).typeahead('val', '');

    if (mute !==  true) {
        this.fire_change_event();
    }

};

TypeaheadTaggingPlugin.prototype.add_to_value = function (value) {

    // adds a tag to the original input's value

    var taglist, // the list of tags, that is currently set as comma separated list on the original input
        added;   // if the tag was added or not

    added = false;
    taglist = this.get_taglist();

    if (taglist.indexOf(value) === -1 && taglist.length < this.max_tags) {
        taglist.push(value);
        added = true;
    }

    this.set_taglist(taglist);

    return added;

};

TypeaheadTaggingPlugin.prototype.append_li = function (value) {

    // takes a string value and appends it as a new tag

    var li,             // the new li element
        tagging_li_new, // the li element holding the typeahead input
        span;           // the span, that is clicked to delete a tag

    // create the new list item
    span = document.createElement('span');
    span.classList.add('tagging_delete_tag');
    span.setAttribute('data-class', 'tagging_delete_tag');
    span.textContent = 'x';

    li = document.createElement('li');
    li.textContent = value;
    li.classList.add('tagging_li');
    li.setAttribute('data-value', value);
    li.setAttribute('title', value);
    li.setAttribute('data-class', 'tagging_tag');
    // append it to the list
    if (this.input !== undefined) {
        tagging_li_new = this.element.parentElement.querySelector('[data-class="tagging_li_new"]');
        tagging_li_new.parentNode.insertBefore(li, tagging_li_new);
    } else {
        this.ul.appendChild(li);
    }
    // TODO this caused problems on load, where the first tag always expanded throught the entire input
    //var i = 0;
    //if (li.offsetWidth > (this.ul.offsetWidth - 35)) {
    //    while (li.offsetWidth > (this.ul.offsetWidth - 35) && i < 100) {
    //        i += 1;
    //        li.textContent = li.textContent.slice(0, li.textContent.length - 4) + '...';
    //    }
    //    li.style.width = '100%';
    //}
    li.appendChild(span);
    // assign click event to span, that should remove the tag
    span.onclick = this.handle_click_delete();

};

TypeaheadTaggingPlugin.prototype.clean_value = function (value) {

    // cleans the value from problematic characters

    return value.replace(this.cleaning_pattern, '');

};


TypeaheadTaggingPlugin.prototype.clear_tags = function (mute) {

    // removes all tags and sets the input value to ''
    var tag_li = this.ul.querySelector('[data-class="tagging_tag"]');
    while (tag_li) {
        tag_li.remove();
        tag_li = this.ul.querySelector('[data-class="tagging_tag"]');
    }
    this.element.value = '';
    if (mute !==  true) {
        this.fire_change_event();
    }
};

TypeaheadTaggingPlugin.prototype.create_li_with_input = function () {

    // append another li with the input

    var li; // the new li element

    // create the new list item
    li = document.createElement('li');
    li.innerHTML = '<input type="text" class="tagging_li_new_input" data-class="tagging_li_new_input" />';
    li.classList.add('tagging_li_new');
    li.setAttribute('data-class', 'tagging_li_new');
    // append it to the list
    this.element.parentElement.querySelector('[data-class="tagging_ul"]').appendChild(li);
    // save the input instance on the plugin
    this.input = li.querySelector('[data-class="tagging_li_new_input"]');
    // assign event handlers to the input
    this.input.onkeyup = this.handle_input_keyup();
    this.input.onkeydown = this.handle_input_keydown();

};

TypeaheadTaggingPlugin.prototype.create_tags = function () {

    // create the initial tags from the value of the input

    var taglist; // the value of the input split at the comma sign to get a list of individual items

    taglist = this.get_taglist();

    this.ul.innerHTML = '';

    for (var i = 0; i < taglist.length; i++) {
        this.append_li(taglist[i]);
    }

};

TypeaheadTaggingPlugin.prototype.create_ul = function () {

    // create the ul that holds the tags and insert it before the original input

    var ul; // the new inserted ul

    ul = document.createElement('ul');
    ul.classList.add('tagging_ul');
    ul.setAttribute('data-class', 'tagging_ul');
    this.element.parentNode.insertBefore(ul, this.element);
    ul.onclick = this.handle_click_to_focus();
    this.ul = ul;

};

TypeaheadTaggingPlugin.prototype.delete_from_value = function (value) {

    // removes a string from the original input's value
    var taglist, // the list of tag strings
        index;   // the index of the value inside the taglist

    if (!value) {
        return false;
    }
    taglist = this.get_taglist();
    index = taglist.indexOf(value);
    if (index !== -1) {
        taglist.splice(index, 1);
    }
    this.set_taglist(taglist);

    return true;

};

TypeaheadTaggingPlugin.prototype.delete_tag = function (value, mute) {

    // removes the tag and the value string from the original input
    if (this.delete_from_value(value)) {
        this.element.parentElement.querySelector('[data-value="' + value + '"]').remove();
    }
    if (mute !==  true) {
        this.fire_change_event();
    }

};

TypeaheadTaggingPlugin.prototype.fire_change_event = function () {

    if ('createEvent' in document) {
        var evt = document.createEvent('HTMLEvents');
        evt.initEvent('change', false, true);
        this.element.dispatchEvent(evt);
    } else {
        this.element.fireEvent('onchange');
    }

};

TypeaheadTaggingPlugin.prototype.get_taglist = function () {

    // returns the value of the original input as an array of tag values

    if (!this.element.value) {
        return [];
    }
    return this.element.value.split(',');

};

TypeaheadTaggingPlugin.prototype.handle_click_to_focus = function () {

    // handles clicks, that should focus on the new tag input
    var that = this;

    return function () {
        that.input.focus();
    };

};

TypeaheadTaggingPlugin.prototype.handle_click_delete = function () {

    // handles clicking of the span, that removes a tag
    var handler;    // the handler, that executes the deletion of the tag
    var that = this;


    handler = function () {
        var value;  // the value of the tag, that should be deleted
        value = this.parentNode.getAttribute('data-value');
        that.delete_tag(value);
    };

    return handler;

};

TypeaheadTaggingPlugin.prototype.handle_input_keyup = function () {

    // handle keyup events
    var handler;    // the event handler function
    var that = this;  // for internal reference inside the handler ('this' becomes the element that causes the event)

    handler = function (e) {
        if (e.keyCode === 13 || e.keyCode === 188) {
            that.add_tag(this.value);
        }
    };

    return handler;
};

TypeaheadTaggingPlugin.prototype.handle_input_keydown = function () {

    // handle keydown events
    var handler,    // the event handler function
        taglist;    // the current list of tags
    var that = this;  // for internal reference inside the handler ('this' becomes the element that causes the event)

    handler = function (e) {
        if (e.keyCode === 9 || e.keyCode === 13) {
            if (this.value && (!that.input.parentNode.querySelector('[class*=tt-hint]').value)) {
                // when enter or tab is pressed
                e.preventDefault();
                that.add_tag(this.value);
            }
        }
        if (e.keyCode === 8) {
            if (!this.value) {
                // when backspace is pressed in an empty input, remove the last tag
                taglist = that.get_taglist();
                that.delete_tag(taglist[taglist.length - 1]);
            }
        }
    };

    return handler;
};

TypeaheadTaggingPlugin.prototype.init = function (tagsource) {

    // create or re-create the input

    // create a wrapper around the input
    var wrapper = document.createElement('div'),
        parent_node = this.element.parentNode,
        next_sibling = this.element.nextSibling;

    wrapper.classList.add('tagging_wrapper');
    wrapper.appendChild(this.element);
    if (next_sibling) {
        parent_node.insertBefore(wrapper, next_sibling);
    }
    else {
        parent_node.appendChild(wrapper);
    }

    // hide the old input
    this.element.style.display = 'none';

    // create the ul that holds the tags
    this.create_ul();

    // create the initial tags from the value of the input
    this.create_tags();

    // append another li with the input
    this.create_li_with_input();

    // initialize typeahead
    this.init_typeahead(tagsource);

};

TypeaheadTaggingPlugin.prototype.init_typeahead = function (tagsource) {

    // initialize typeahead for the input
    if (tagsource) {


        jQuery(this.input).typeahead(
            {
                hint     : true,
                highlight: true,
                minLength: 1
            },
            {
                name      : this.typeahead_datasetname,
                displayKey: 'value',
                source    : this.substringMatcher(tagsource)
            }
        );
    }
};

TypeaheadTaggingPlugin.prototype.set_taglist = function (taglist) {

    // saves an array of tag strings as value on the original input

    this.element.value = taglist.join();

};

TypeaheadTaggingPlugin.prototype.set_value = function (taglist) {

    // takes an array of strings as an input and replaces the value and all tags with it
    this.clear_tags(true);
    for (var i = 0; i < taglist.length; i++) {
        this.add_tag(taglist[i], true);
    }
    // we muted the change event so far and fire it now only once
    this.fire_change_event();

};

TypeaheadTaggingPlugin.prototype.substringMatcher = function (tagsource) {

    var that = this;

    return function findMatches(q, cb) {
        var matches, substrRegex, values, taglist;

        // an array that will be populated with substring matches
        matches = [];

        // the values left for completion. Excludes the ones already being set as value on the input.
        values = [];

        // regex used to determine if a string contains the
        // substring `q`
        substrRegex = new RegExp(q, 'i');

        // iterate through the pool of strings and for any string
        // that contains the substring `q`, add it to the `matches`
        // array
        taglist = that.get_taglist();
        for (var i = 0; i < tagsource.length; i++) {
            if (taglist.indexOf(tagsource[i]) === -1) {
                values.push(tagsource[i]);
            }
        }

        jQuery.each(values, function (i, str) {
            if (substrRegex.test(str)) {
                matches.push({value: str});
            }
        });

        cb(matches);
    };
};

(function ($) {
    $.fn.tagging = function (arg, arg2) {
        var plugin,     // the plugin instance
            plugin_name = 'plugin_tagging';
        if (arg) {
            if ($.isArray(arg)) {
                return this.each(function () {
                    plugin = $.data(this, plugin_name);
                    if (typeof plugin === 'undefined') {
                        plugin = new TypeaheadTaggingPlugin(this);
                        $.data(this, plugin_name, plugin);
                        plugin.init(arg);
                    }
                    return plugin;
                });
            } else if (arg === 'clear') {
                plugin = $.data(this[0], plugin_name);
                return plugin.clear_tags();
            } else if (arg === 'value' && typeof arg2 === 'undefined') {
                plugin = $.data(this[0], plugin_name);
                return plugin.get_taglist();
            } else if (arg === 'value' && typeof $.isArray(arg2)) {
                plugin = $.data(this[0], plugin_name);
                plugin.set_value(arg2);
                return plugin;
            }
        } else {
            // if the plugin is called without tag source, return the plugins itself
            return $.data(this[0], plugin_name);
        }
    };
})(jQuery);
