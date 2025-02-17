def explanation_corr(val):
    if  0 <= val :
        tmp_str = "正"
    else :
        tmp_str = "負"
        
    if 0.7 <= abs(val) <= 1.0:
        exp_str = f"強い{tmp_str}の相関がある"
    elif 0.4 <= abs(val) < 0.7:
        exp_str = f"中程度の{tmp_str}の相関がある"
    elif 0.2 <= abs(val) < 0.4:
        exp_str = f"弱いの{tmp_str}の相関がある"
    elif 0.0 <= abs(val) < 0.2:
        exp_str = f"ほぼ相関はない"
    return exp_str