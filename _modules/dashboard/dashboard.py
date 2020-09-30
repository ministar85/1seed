from init import *

dashboard = Blueprint("dashboard", __name__, static_folder="static", template_folder="templates")

@dashboard.route('/<string:dropdown>/', methods =['GET', 'POST']) 
def home(dropdown):
    #sensorsdata, selcet db
    sensorsdata = "sensorsdata"

    #Create Cursor
    cur = mysql.connection.cursor()

    #Get Storage Items
    a = session['username']

    if request.args.get('graphtype') :
        print("...getting values from ajax")
        dropdown = request.args.get('graphtype')
    #else :
    #    dropdown = 'default'
    
    print("-------chosen from drop down:",dropdown)
    print("-------********")

    ########################################################################################################################
    #################################### Get Outdooor Temperature  #########################################################
    ########################################################################################################################

    #cur.execute('SELECT temperature_outdoor,date_measured FROM sensorsdata WHERE username = %s order by id desc limit 12;',[a])

    if dropdown == 'default':
        cur.execute('SELECT temperature_outdoor,date_measured FROM sensorsdata WHERE username = %s and temperature_outdoor IS NOT NULL order by id desc limit 10;',[a])
        result = 'default'

    if dropdown == 'live':
        print("entered live")
        result = 'live'
        cur.execute('SELECT temperature_outdoor,date_measured FROM sensorsdata WHERE username = %s and temperature_outdoor IS NOT NULL order by id desc limit 10;',[a])
    
    if dropdown == 'last day':
        print("entered last day")
        result = 'last day'
        cur.execute('SELECT hour(`date_measured`) as Period,round(sum(`temperature_outdoor`)/count(hour(`date_measured`)),2) as Average FROM  `sensorsdata` where username = %s and temperature_outdoor IS NOT NULL and (date(date_measured) = CURDATE() or date(date_measured) = CURDATE() - 1) GROUP BY day(`date_measured`),hour(`date_measured`)  order by id desc limit 24;',[a])

    if dropdown == 'last week':
        #cur.execute('SELECT temperature_outdoor,date_measured FROM sensorsdata WHERE username = %s order by id desc limit 2;',[a])
        cur.execute('SELECT DAYNAME(`date_measured`) as Period,round(sum(`temperature_outdoor`)/count(DAYNAME(`date_measured`)),2) as Average FROM sensorsdata where username = %s and temperature_outdoor IS NOT NULL GROUP BY dayofweek(`date_measured`) limit 7;',[a])
        result = 'last week'
        #return jsonify(result='last week')
    if dropdown == 'last year':
        #cur.execute('SELECT temperature_outdoor,date_measured FROM sensorsdata WHERE username = %s order by id desc limit 15;',[a])
        cur.execute('SELECT monthname(`date_measured`) as Period,round(sum(`temperature_outdoor`)/count(month(`date_measured`)),2) as Average FROM  `sensorsdata` where username = %s and temperature_outdoor IS NOT NULL GROUP BY month(`date_measured`) ORDER BY month(`date_measured`) desc limit 12;',[a])
        result = 'last year'
    
    temperaturesOutdoor = cur.fetchall()

    temperatureOutdoor_values = list()
    temperatureOutdoor_timestamp = list()
    temperatureOutdoor_time = list()
    temperatureOutdoor_date = list()
    temperatureOutdoor_xaxis = list()
    temperatureOutdoor_yaxis = list()

    tempmaxoutdoor = 0
    ##define max for the sensor:
    tempminoutdoor = 60
    
    if dropdown == 'last week' or dropdown == 'last year' or dropdown == 'last day': 
        for row in temperaturesOutdoor:
            #calculating min/max for the period
            if row["Average"] > tempmaxoutdoor:
                tempmaxoutdoor = row["Average"]
            if row["Average"] < tempminoutdoor:
                tempminoutdoor = row["Average"]    
            ###############################
            print("-------")
            print("temperatureOutdoor :",row["Average"])
            temperatureOutdoor_values.append(row["Average"])
            #define x axis for printing to graph:
            temperatureOutdoor_xaxis.append(row["Period"])
            print("Period :",row["Period"])

        #define y axis for printing to graph:
        temperatureOutdoor_yaxis = temperatureOutdoor_values
        #define graph max:
        line_valuesOutdoor = temperatureOutdoor_yaxis
        temperatureOutdoor_timestamp = temperatureOutdoor_xaxis    
    

    else:
        for row in temperaturesOutdoor:
            #calculating min/max for the period
            if row["temperature_outdoor"] > tempmaxoutdoor:
                tempmaxoutdoor = row["temperature_outdoor"]
            if row["temperature_outdoor"] < tempminoutdoor:
                tempminoutdoor = row["temperature_outdoor"]    
            ###############################
            print("-------")
            print("temperatureOutdoor :",row["temperature_outdoor"])
            temperatureOutdoor_values.append(row["temperature_outdoor"])

            timestampOutdoor = row["date_measured"]
            timestampOutdoor = str(timestampOutdoor)
            print("timestampOutdoor :",timestampOutdoor)
            dateOutdoor, timeOutdoor = timestampOutdoor.split()
            print("dateOutdoor :",dateOutdoor)
            print("timeOutdoor :",timeOutdoor)
            temperatureOutdoor_timestamp.append(timestampOutdoor)
            temperatureOutdoor_time.append(timeOutdoor)
            temperatureOutdoor_date.append(dateOutdoor)
        
        #define x axis for printing to graph:
        temperatureOutdoor_xaxis = temperatureOutdoor_time
        #define y axis for printing to graph:
        temperatureOutdoor_yaxis = temperatureOutdoor_values

        #define graph max:
        line_valuesOutdoor = temperatureOutdoor_yaxis
        temperatureOutdoor_timestamp = temperatureOutdoor_xaxis
    
    ########################################################################################################################
    ########################################################################################################################


    ########################################################################################################################
    #################################### Get Indoor Temperature  #########################################################
    ########################################################################################################################
    
    #result = cur.execute('SELECT value FROM temperature WHERE username = %s',[a])
    
    #cur.execute('SELECT temperature_indoor,date_measured FROM sensorsdata WHERE username = %s order by id desc limit 3;',[a])

    #    lang = request.args.get('graphtype', 0, type=str)
    #lang = request.args.get('graphtype', 0, type=str)

   
    if dropdown == 'default':
        cur.execute('SELECT temperature_indoor,date_measured FROM sensorsdata WHERE username = %s order by id desc limit 10;',[a])
        result = 'default'

    if dropdown == 'live':
        print("entered live")
        result = 'live'
        cur.execute('SELECT temperature_indoor,date_measured FROM sensorsdata WHERE username = %s and temperature_indoor IS NOT NULL order by id desc limit 10;',[a])
    
    if dropdown == 'last day':
        print("entered last day")
        result = 'last day'
        cur.execute('SELECT hour(`date_measured`) as Period,round(sum(`temperature_indoor`)/count(hour(`date_measured`)),2) as Average FROM  `sensorsdata` where username = %s and temperature_indoor IS NOT NULL and (date(date_measured) = CURDATE() or date(date_measured) = CURDATE() - 1) GROUP BY day(`date_measured`),hour(`date_measured`)  order by id desc limit 24;',[a])

    if dropdown == 'last week':
        cur.execute('SELECT DAYNAME(`date_measured`) as Period,round(sum(`temperature_indoor`)/count(DAYNAME(`date_measured`)),2) as Average FROM sensorsdata where username = %s and temperature_indoor IS NOT NULL GROUP BY dayofweek(`date_measured`) limit 7;',[a])
        result = 'last week'
        #return jsonify(result='last week')
    if dropdown == 'last year':
        #cur.execute('SELECT temperature_indoor,date_measured FROM sensorsdata WHERE username = %s and temperature_indoor IS NOT NULL order by id desc limit 15;',[a])
        cur.execute('SELECT monthname(`date_measured`) as Period,round(sum(`temperature_indoor`)/count(month(`date_measured`)),2) as Average FROM  `sensorsdata` where username = %s and temperature_indoor IS NOT NULL GROUP BY month(`date_measured`) ORDER BY month(`date_measured`) desc limit 12;',[a])        
        result = 'last year'
        #return jsonify(result='last year')
    #if dropdown == 'custom':
        #return jsonify(result='custom')
        
    
    #print("---calculating results from sql response")
        
    temperatures = cur.fetchall()

    temperature_values = list()
    temperature_timestamp = list()
    temperature_time = list()
    temperature_date = list()
    temperature_xaxis = list()
    temperature_yaxis = list()

    tempmaxindoor = 0
    ##define max for the sensor:
    tempminindoor = 60
    
    if dropdown == 'last week' or dropdown == 'last year' or dropdown == 'last day':
        for row in temperatures:
            #calculating min/max for the period
            if row["Average"] > tempmaxindoor:
                tempmaxindoor = row["Average"]
            if row["Average"] < tempminindoor:
                tempminindoor = row["Average"]    
            ###############################
            print("-------")
            print("temperature :",row["Average"])
            temperature_values.append(row["Average"])
            #define x axis for printing to graph:
            temperature_xaxis.append(row["Period"])
            print("Period :",row["Period"])
        #define y axis for printing to graph:
        temperature_yaxis = temperature_values
        #define graph max:
        line_values = temperature_yaxis
        temperature_timestamp = temperature_xaxis
    else:
        for row in temperatures:
            #calculating min/max for the period
            if row["temperature_indoor"] > tempmaxindoor:
                tempmaxindoor = row["temperature_indoor"]
            if row["temperature_indoor"] < tempminindoor:
                tempminindoor = row["temperature_indoor"]    
            ###############################
            #print("-------")
            #print("temperature :",row["temperature_indoor"])
            temperature_values.append(row["temperature_indoor"])

            timestamp = row["date_measured"]
            timestamp = str(timestamp)
            #print("timestamp :",timestamp)
            date, time = timestamp.split()
            #print("date :",date)
            #print("time :",time)
            temperature_timestamp.append(timestamp)
            temperature_time.append(time)
            temperature_date.append(date)
        
        #define x axis for printing to graph:
        temperature_xaxis = temperature_time
        #define y axis for printing to graph:
        temperature_yaxis = temperature_values

        line_values = temperature_yaxis
        temperature_timestamp = temperature_xaxis
    
    #define graph max:
    max=40

    cur.close()
    
    #radi: return render_template('dashboard.html', title='Greenhouse temperature indoor', max=max, labels=temperature_xaxis, values=line_values, title1='Greenhouse temperature outdoor', labels1=temperatureOutdoor_xaxis, values1=line_valuesOutdoor)
            
    if dropdown == 'default': 
        return render_template('dashboard.html', title='Greenhouse temperature indoor',tempmaxoutdoor = tempmaxoutdoor, tempminoutdoor = tempminoutdoor, tempmaxindoor = tempmaxindoor, tempminindoor = tempminindoor, max=max, labels=temperature_xaxis, values=line_values, title1='Greenhouse temperature outdoor', labels1=temperatureOutdoor_xaxis, values1=line_valuesOutdoor, dropdown=dropdown)
    else :
        return render_template('dashboard.html', title='Greenhouse temperature indoor',tempmaxoutdoor = tempmaxoutdoor, tempminoutdoor= tempminoutdoor, tempmaxindoor = tempmaxindoor, tempminindoor = tempminindoor, max=max, labels=temperature_xaxis, values=line_values, title1='Greenhouse temperature outdoor', labels1=temperatureOutdoor_xaxis, values1=line_valuesOutdoor, dropdown=dropdown)
        return redirect(url_for('dashboard.home', dropdown=dropdown))

