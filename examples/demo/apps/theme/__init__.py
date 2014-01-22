from uliweb.contrib.template.tags import LinkNode

class TemplateUtils(object):
    out = None
    def set_out(self, out):
        self.out = out
        
    def theme(self):
        self.out.xml(get_current_themem())

    def set_current_menu(self, current="photos"):
        self.current = current

    def navmenu(self, current=None, head=False):
        from uliweb import settings

        current = current or self.current

        menus = settings.get_var("GLOBAL/NAV_MENU")
        out = self.out

        out.xml('<ul class="nav">')

        is_first = True
        for menu in menus:
            (id, link, text, icon) = (menu['id'], menu['link'], menu['text'], menu['icon'])

            klass = None
            if not head:
                text = '<span class="%s"></span>&nbsp;%s' % (icon, text)
            else:
                text = '<span class="%s" title="%s"></span>' % (icon, text)

            if is_first:
                if id == current :
                    klass = "first active"
                else:
                    klass = "first"
                is_first = False
            else:
                if id == current :
                    klass = "active"                    
                else:
                    klass = ""

            out.xml('<li class="%s"><a href="%s">%s</a></li>' %(klass, link, text))
        out.xml('</ul>')

            
class ThemeLinkNode(LinkNode):
    def __init__(self, value=None, content=None, template=None):
        value = value.replace("<THEME>", get_current_themem())
        super(ThemeLinkNode, self).__init__(value, content, template)
        
def get_current_themem():
    from uliweb import settings
    return settings.THEME.CURR_THEME

def get_utils(out):
    utils = TemplateUtils()
    utils.set_out(out)
    return utils
    
def startup_installed(sender):
    from uliweb.core import template
    template.register_node('themelink', ThemeLinkNode)
    
