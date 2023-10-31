import streamlit as st
from arduino import write, close ,ini, activeCOMS, read
#import atexit
import time

def store_session():
    for k, v in this.items():
        this[k] = v
        return

st.set_page_config(
    page_icon="images/mantra_logo_inverted.png",
    page_title="Mantra",
    initial_sidebar_state="expanded",
)
this = st.session_state

left,center,right = st.columns(3)


#################################
#                               #
#       Arduino Functions       #
#                               #
#################################

def arduinos(data):
    ini(data)
    with left:
        with st.spinner("Connecting to Arduino"):
            time.sleep(2)
            write('getState')
            while True:
                recv = read()
                print(recv)
                if '!' in recv.decode('utf-8'):
                    break
    st.toast(f"Arduino Connection Accepted.",icon="✅")
    st.toast(f"Port: {data}, BaudRate: 115200",icon="✅")
    this.arduinoActive = True
    store_session()

def ARDwrite(data):
    write(data)
    store_session()
    return
    
def ARDclose():
    with left:
        with st.spinner("Closing Arduino Port"):
            time.sleep(2)
            close()
    store_session()
    if 'arduinoActive' in this:
        #arduino.close()
        del this['arduinoActive']
        this.clear()

#********************************#

#################################
#                               #
#       Extra Functions         #
#                               #
#################################



def ss_det():
    print(this)
    store_session()

def gg_det():
    if 'arduino' in globals():
        print(globals(['arduino']))
    else:
        print("Dokoooo daaaaaa")
    store_session()


#################################
#                               #
#           Pages               #
#                               #
#################################

def set_main_page(working_page):
    this.page = working_page
    store_session()

def home():
    header()
    col1 , col2 ,col3 = st.columns([0.5,0.5,1])
    with col3:
        st.button("Exit",on_click=ARDclose)

    if 'arduinoActive' not in this:
        COMSelect = activeCOMS()
        if len(COMSelect) != 0:
            this['arduino'] = COMSelect[0]
            with col1:
                st.button(f"Connect: {this.arduino}",on_click=arduinos,args=[this.arduino], use_container_width=True)
        else:
            st.write('No Arduino Connection Found.')
    else:
        if 'user' not in this:
            st.text("हरियो बत्ती अगाडि आफ्नो कार्ड पेश गर्नुहोस्  ")
            get = ''
            time.sleep(1)

            while True:
                write('getRFIDuser')
                get = read()
                recv = get.decode('utf-8')
                print(recv)
                if len(recv) != 0:
                    break
            this.user = recv.split(":")[1].strip()
            st.rerun()
        else:
            with col1:
                st.button("Inorganic",on_click=set_main_page,args=['inorganic'])
            with col2:
                st.button("Organic",on_click=set_main_page,args=['organic'])

def inorganic():
    header()
    st.header("Inorganic")
    st.text("Inorganic Total Weight = 21.59 kg")
    write('inorganic')
    wt = read().decode('utf-8')
    print(wt)
    weight_inorganic = wt.split(':')[1].strip()
    st.text(f"Today's Capacity: {weight_inorganic} kg")
    
    st.button("Exit to Main",on_click=set_main_page,args=['home'])
    
    ARDwrite("on")

def organic():
    header()
    st.header("Organic")
    st.text("Organic Total Weight = 21.59 kg")

    write('organic')
    wt = read().decode('utf-8')
    weight_inorganic = wt.split(':')[1].strip()
    st.text(f"Today's Capacity: {weight_inorganic} kg")
    
    st.button("Exit to Main",on_click=set_main_page,args=['home'])
    ARDwrite("off")

def header():
    left,center,right = st.columns(3)
    if this.page == 'home':
        with center:
            st.image(image="images/mantra_logo_inverted.png",caption="Mantra INC.",width=100)
    
        st.header("Waste Management System")
        if 'user' not in this:
            st.subheader("नमस्कार 🙏")
        else:
            st.subheader(f"नमस्कार {this.user}🙏")
    else:
        with left:
            st.image(image="images/mantra_logo_inverted.png",caption="Mantra INC.",width=50)
        with center:
            st.subheader("Waste Management System")

def set_language(lan):
    this.language = lan
    this.page = 'home'
    
def languageSelect():
    header()
    st.header("Select Language / भाषा छनोट गर्नुहोस्।")
    column1 , column2 ,column3 , column4= st.columns(4)
    with column1:
        st.button('ENGLISH',on_click=set_language,args=['ENG'])
    with column2:
        st.button('नेपाली',on_click=set_language,args=['NEP'])
    

#################################
#                               #
#       Program Start           #
#                               #
#################################


Pages = {
    'languageSelect':languageSelect,
    'home':home,
    'inorganic': inorganic,
    'organic': organic 
    }

if 'page' not in this:    
    if 'language' not in this:
        this.page = 'languageSelect'
    else:
        this.page = 'home'

if 'language' in this:
    st.text(this.language)

pageToShow = Pages.get(this.page)
pageToShow()
    
    #Blink Functionss
    #blinkCol1 , blinkCol2 = st.columns([0.5,1])
    #with blinkCol1:
    #    st.number_input("",key='blink',step=1,on_change=store_session)
    #with blinkCol2:
    #    if 'blink' in st.session_state:
    #        #print(f'blink {st.session_state.blink}')
    #        st.button("Blink",on_click=callwrite,args=[f'blink {st.session_state.blink}'])
        