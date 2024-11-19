def get_css(temp):
     
     temp_max = float(temp)
     
     if temp_max<=0:
          return "c0" 
     elif temp_max <=10 and temp_max > 0:
          return "c10"
     
     elif temp_max <=15 and temp_max >10:
          return "c15"
     
     
     elif temp_max <=20 and temp_max > 15:
          return "c20"
     elif temp_max <=25 and temp_max > 20:
          return "c25"
     elif temp_max <=30 and temp_max > 25:
          return "c30"
     
     elif  temp_max > 30:
          return "c35"
     