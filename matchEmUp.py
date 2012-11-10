'''
Created on Oct 17, 2012

@author: Jason

'''
#import re
#import wx
import os

class Matcher(object):
    """Methods to find and group files in a specified directory.
    Intended usage is to list all files in a specified directory,
    then attemp to separate them into the following groups:
        Banners
        Landings    (up to 3 lp files)
        URLs
        Capture file
        Other
        """
    def __init__(self):
        self.desktop = (os.environ['USERPROFILE'] + '\\Desktop\\')
        self.home = 'c:/users/jason/desktop/mobtests/'
        self.folder = 'mobtests\\'
        self.placeholder_list = []
        self.banners = []
        self.landings = []
        self.urls = []
        self.capture = []
        self.other = []
        self.advertisers = []
        self.file_dict = {}
        self.categories = ["banner", "landing", "landing2", "landing3",
                           "url"]
        self.other_list = [self.banners, self.landings, self.landings, 
                           self.landings, self.urls, self.capture]

    def listfiles(self, path):
        """List all files in path"""
        return os.listdir(path)

    def populate_lists(self, alist):
        """ Populates the main lists of the Match method.
        Note: the listfiles method should be run first."""
        pass

    def clear_lists(self):
        """Empties all lists"""
        self.__init__()

    def find_banners(self, alist):
        """Find banner ads in self.placeholders list. """
        temp = []
        for item in alist:
            if '-banner.' in item.lower():
                temp.append(item)
        return temp

    def list_banners(self, alist):
        """Moves banner ads to the banners list. Removes them
        from self.placeholder_list and adds them to self.banners list"""
        temp = self.find_banners(alist)
        for item in temp:
            if item in alist:
                self.banners.append(alist.pop(alist.index(item)))
            else:
                continue

    def find_landings(self, alist):
        """Find landing page files in alist"""
        temp = []
        for item in alist:
            if '-landing' in item.lower():
                temp.append(item)
        return temp

    def list_landings(self, alist):
        """Moves landings to the landings list"""
        temp = self.find_landings(alist)
        for item in temp:
            if item in alist:
                self.landings.append(alist.pop(alist.index(item)))
            else:
                continue

    def find_urls(self, alist):
        """Find url files in self.placeholders list"""
        temp = []
        for item in alist:
            if '-url' in item.lower():
                temp.append(item)
        return temp

    def list_urls(self, alist):
        """Moves url files to the URL list"""
        temp = self.find_urls(alist)
        for item in temp:
            if item in alist:
                self.urls.append(alist.pop(alist.index(item)))
            else:
                continue

    def find_captures(self, alist):
        """Finds url files in self.placeholders list"""
        temp = []
        for item in alist:
            if '-capture' in item:
                temp.append(item)
        return temp

    def list_captures(self, alist):
        """Moves capture files from self.placeholders list
        to self.capture list"""
        temp = self.find_captures(alist)
        for item in temp:
            if item in alist:
                self.capture.append(alist.pop(alist.index(item)))
            else:
                continue
    def list_ads(self):
        """Gets the names of the advertisers, minus the '-banner'"""
        for item in self.banners:
            split = item.split('-')
            #if split[0] in self.advertisers:                 
            self.advertisers.append(split[0])
            
            
    def list_other(self, alist):
        """Lists the files that are left over. Must be run after all
        other lists are populated
        Note: this will clear all contents of alist""" 
        length = len(alist)
        while length > 0:
            self.other.append(alist.pop(0))
            length -= 1
        

    def listall(self, path):
        self.placeholder_list = self.listfiles(path)
        self.list_banners(self.placeholder_list)
        self.list_landings(self.placeholder_list)
        self.list_urls(self.placeholder_list)
        self.list_captures(self.placeholder_list)
        self.list_other(self.placeholder_list)
        self.list_ads()
        self.sort_it()
        
    def sort_it(self):
        """ Creates a dictionary based on the self.advertisers list.
        the keys in the dict are advertiser names,
        values are lists [banner, landing1, landing2, landing3, url"""
        for advertiser in self.advertisers:
            count = 0
            temp_list = []
            for category in self.categories:  # Break this part out into a separate method.
                temp_list.append("Temp")
                
                for item in self.other_list[count]:
                    split_ext = item.split('.')
                    split_dash = split_ext[0].split('-')
                    
                    if split_dash[0].lower() == advertiser.lower() and split_dash[1].lower() == category.lower():
                        temp_list[count] = item
                        count += 1
                        break
                    else:
                        continue
                try:
                    if temp_list[count] == "Temp":
                        temp_list[count] = "None"
                        count += 1
                except IndexError:
                    if temp_list[count - 1] == "Temp":
                        temp_list[count - 1] = "None"
            self.file_dict[advertiser] = temp_list

            
    def matched_list(self, advertiser, other_list, cat_list ):
        pass            
        

def main():
    """test the Match class"""
    m = Matcher()
    m.listall((m.desktop + m.folder))

    # Un-comment the section below to print the lists.
    
    print "Advertisers are"
    print m.advertisers
    print "Banners are:"
    print m.banners
    print "Landing Pages:"
    print m.landings
    print "URLs:"
    print m.urls
    print "Capture Files:"
    print m.capture
    print "Other:"
    print m.other
    print "At the end, Placeholder List is now:"
    print m.placeholder_list
    
    m.sort_it()
    print m.file_dict

if __name__ == '__main__':
    main()