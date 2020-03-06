def make_page_button(label, link, active=False, disabled=False, aria_label=None, sr_hide=False, sr_label=None):

    if active:
        li_active = ' active';
        sr_label = '(current)';
    else:
        li_active = '';

    if disabled:
        li_disabled = ' disabled';
        a_disabled = r' tabindex="-1"';
        a_url = '#';
    else:
        li_disabled = '';
        a_disabled = '';
        a_url = link;

    if aria_label:
        a_aria = r' aria-label="' + aria_label + r'"';
    else:
        a_aria = '';

    if sr_hide:
        label = r'<span aria-hidden="true">' + label + '</span>';

    if sr_label:
        span_sr_label = r'<span class="sr-only">' + sr_label + '</span>';
    else:
        span_sr_label = '';

    output = r"""
<li class="page-item%s%s">
    <a class="page-link" href="%s"%s%s>
        %s %s
    </a>
</li>
""" % (li_active, li_disabled, a_url, a_disabled, a_aria, label, span_sr_label);

    return output


def make_page_navbar(num_pages, current_page, base_url, label):
    navbar = r"""<nav aria-label="%s"><ul class="pagination justify-content-center">""" % label;

    if current_page == 1:
        prev_link = '#';
        prev_d = True;
    else:
        prev_link = base_url + "%d" % (current_page-1);
        prev_d = False;

    navbar += make_page_button('&laquo;', prev_link, disabled=prev_d, aria_label='Previous', sr_hide=True, sr_label='Previous');

    for p in range(1, num_pages+1):
        if p == current_page:
            p_active = True;
        else:
            p_active = False;

        navbar += make_page_button(p, base_url + "%d" % p, active=p_active);

    if current_page == num_pages:
        next_link = '#';
        next_d = True;
    else:
        next_link = base_url + "%d" % (current_page+1);
        next_d = False;

    navbar += make_page_button('&raquo;', next_link, disabled=next_d, aria_label='Next', sr_hide=True, sr_label='Next');

    navbar += "</ul></nav>";

    return navbar;


def encode_for_json(unencoded):
    return unencoded.replace("\n","").replace('"',r'\"');
