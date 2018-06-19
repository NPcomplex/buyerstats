'''
Created on May 28, 2018

@author: Natty
'''
from utilities import write_dict_to_csv
from query.card_data import TcgApiQueryMachine

def create_pricing_csv_from_deckstats(deckstats_filename, csv_filename, price_type):
    '''
    '''
    cardlist_dict = create_cardlist_dict_from_deckstats(deckstats_filename)
    min_price_dict = get_min_price_dict(cardlist_dict, price_type)
    
    write_dict_to_csv(min_price_dict, csv_filename)

#create a dictionary of the pricing data given a list of cards and their quantity and the desired price type
def get_min_price_dict(cardlist_dict, price_type):
    '''
    create a pricing dictionary for these cards
    '''
    api_query_machine = TcgApiQueryMachine()
    price_dict = {}
    for cardname in cardlist_dict:
        min_product_id, min_type, min_price = api_query_machine.find_min_price(cardname, price_type)
        price_dict[cardname] = min_price
        
    return price_dict
    
def get_total_price_dict(cardlist_dict, price_type):
    '''
    create a dictionary with the minumum price (price_type) of cards at the quantity listed in cardilst_dict
    TODO create if needed
    '''
    
#create a cardlist dictionary from a file in deckstats export format (format follows)
# //this is a comment
# quantity cardname (on each line)
# "# !Commander" might be at the end of a line and could be removed
def create_cardlist_dict_from_deckstats(filename):
    '''
    '''
    cardlist_dict = {}
    with open(filename, 'r') as deckfile:
        for line in deckfile:
            #only process the line if it is not a comment and it is not a empty line
            if not (line.startswith( '//') or len(line.strip()) == 0 or line.startswith( 'SB')):
                line_has_count = line.strip()[0].isdigit()
                cardcount_break_index = line.find(' ') if line_has_count else 0
                card_count = int(line[:cardcount_break_index].strip()) if line_has_count else 1
                commander_break_index = line.find('#')
                
                #use cardname_not_found to indicate that there was a row with no cardname in it
                #what should we do in this case? mostly just ignoring it for now
                cardname = 'cardname_not_found'
                if commander_break_index != -1:
                    cardname = line[cardcount_break_index:commander_break_index-1].strip()
                else:
                    cardname = line[cardcount_break_index:].strip()
                
                cardlist_dict[cardname] = card_count
            
    return cardlist_dict        
    
    
if __name__ == '__main__':
    create_pricing_csv_from_deckstats(r'C:\development\TCGPlayer_api\buyer_stats\jodah_ideas.txt', r'C:\development\TCGPlayer_api\buyer_stats\jodah_thoughts.csv', 'marketPrice')