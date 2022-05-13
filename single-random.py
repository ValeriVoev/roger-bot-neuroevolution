# Import libraries


def calculate_bot_assumptions(player, zopa_min_buyer, zopa_max_buyer, zopa_min_seller, zopa_max_seller):
    
    ora_amount = (
        zopa_max_buyer 
        if player.role == "seller" 
        else zopa_min_seller
        )
    rs_amount = (
        (player.batna + (zopa_max_buyer + zopa_min_buyer)/2)/2
        if player.role == "seller" 
        else (player.batna + (zopa_max_seller + zopa_min_seller)/2)/2
    )

    return {
        "ORA": {
            "amount": ora_amount,
            "percentage": 30
        },
        "RS": {
            "amount": rs_amount,
            "percentage": 50
        }
    }