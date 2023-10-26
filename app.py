import streamlit as st
from arduino import write, close ,ini, activeCOMS, read
import atexit
import time

#global arduino
this = st.session_state

def store_session():
    for k, v in this.items():
        this[k] = v

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
#       Program Start           #
#                               #
#################################


def exit_function():
    ARDclose()    

atexit.register(exit_function)

st.set_page_config(
    page_icon="images/mantra_logo_inverted.png",
    page_title="Mantra"
)
left,center,right = st.columns(3)
with center:
    st.image(image="images/mantra_logo_inverted.png",caption="Mantra INC.",width=100)
st.header("Waste Management System")
if 'user' not in this:
    st.subheader("नमस्कार 🙏")
else:
    st.subheader(f"नमस्कार {this.user}🙏")


#st.toggle()
#st.expander()
st.header("")

col1 , col2 ,col3 = st.columns([0.5,0.5,1])
with col3:
    st.button("Exit",on_click=ARDclose)

#st.button("Session Details",on_click=ss_det)
#st.button("Globals Details",on_click=gg_det)

if 'arduinoActive' not in this:
    COMSelect = activeCOMS()
    if len(COMSelect) != 0:
        #arduinos(COMSelect[0])
        ##Wait for RFID if data is obtained then rerun
        #time.sleep(3)
        #st.rerun()
        #st.selectbox("Select Port:",options=COMSelect,key='arduino')
        #st.text(f"Using Arduino COM Port: {this.get('arduino')}")
        this['arduino'] = COMSelect[0]
        with col1:
            st.button(f"Connect: {this.arduino}",on_click=arduinos,args=[this.arduino], use_container_width=True)
    else:
        st.write('No Arduino Connection Found.')
else:
    #st.text(f"Using Arduino COM Port: {this.get('arduino')}")
    if 'user' not in this:
        st.text("हरियो बत्ती अगाडि आफ्नो कार्ड पेश गर्नुहोस्  ")
        get = ''
        
        #get = read()
        while True:
            write('getRFIDuser')
            get = read()
            recv = get.decode('utf-8')
            print(recv)
            if len(recv) != 0:
                break
        this.user = recv.split(":")[1].strip()
        st.rerun()
        #name = 'Sameer Timsina'
    with col1:
        st.button("Inorganic",on_click=ARDwrite,args=['on'])
    with col2:
        st.button("Organic",on_click=ARDwrite,args=['off'])
    





    
    #Blink Functionss
    #blinkCol1 , blinkCol2 = st.columns([0.5,1])
    #with blinkCol1:
    #    st.number_input("",key='blink',step=1,on_change=store_session)
    #with blinkCol2:
    #    if 'blink' in st.session_state:
    #        #print(f'blink {st.session_state.blink}')
    #        st.button("Blink",on_click=callwrite,args=[f'blink {st.session_state.blink}'])
        