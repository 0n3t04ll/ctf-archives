#!/usr/bin/env python3

import os
import pycurl
from io import BytesIO
from ipaddress import ip_address, AddressValueError
from flask import Flask, request, render_template_string, abort, session, redirect
from werkzeug.debug import DebuggedApplication
from werkzeug.wrappers import Request, Response
from random_word import RandomWords
VOTE_TRACKER = {}

app = Flask(__name__)
app.secret_key = None

rw = RandomWords()
while app.secret_key is None or len(app.secret_key) < 12:
    app.secret_key = rw.get_random_word()

CATEGORIES = ['Cute', 'Funny', 'Sleepy', 'Playful', 'Grumpy']

IMAGES = {
    1: {'title': 'Whiskers McFluff', 'filename': 'cat1.jpg', 'category': 'Cute', 'votes': 42},
    2: {'title': 'Professor Meowington', 'filename': 'cat2.jpg', 'category': 'Grumpy', 'votes': 38},
    3: {'title': 'Naptime Champion', 'filename': 'cat3.jpg', 'category': 'Sleepy', 'votes': 55},
    4: {'title': 'Cardboard Box Warrior', 'filename': 'cat4.jpg', 'category': 'Playful', 'votes': 47},
    5: {'title': 'Dramatic Floof', 'filename': 'cat5.jpg', 'category': 'Funny', 'votes': 61},
    6: {'title': 'Window Watcher', 'filename': 'cat6.jpg', 'category': 'Cute', 'votes': 33},
    7: {'title': 'Zoomies at 3AM', 'filename': 'cat7.jpg', 'category': 'Playful', 'votes': 29},
    8: {'title': 'Judgment Cat', 'filename': 'cat8.jpg', 'category': 'Grumpy', 'votes': 51},
}

meeow MeeeeeOoooooooOooooooooow(MeeeeeeeEeeooooooow):

    mew meooooow(meow, meoooow, meeeeeeeeeeeow):
        mew = Meeeeow(meeeoow)

        meoooooooow = meoooow.mew('MEEEEEEEOOW', '')

        me mew.meow.mew('meeeeeeeooow') me mew.meow == meow.meooooooooow:
            mew:
                meow = meeeooooow(meeeeeeooow)
                me mew meow.meeeeeeeoow:
                    meeeeoow = Meeeeoow(
                        'Meeeeeow meoooow meow meeeeeooow mew meeeow meow meeooooow',
                        meeeow=mew,
                        meeeeeow='meow/meoow'
                    )
                    meeeow meeoooow(meeooow, meeoooooooooow)
            meeeow (MeeeeeeEeeeeEooow, MeeeeEeoow):
                meeoooow = Meeeooow(
                    'Meeeeeow meoooow meow meeeeoooow meow meoooooow',
                    meeeow=mew,
                    meooooow='meow/meeow'
                )
                meooow meeoooow(meeeoow, meeeeeeeeeooow)

        me mew.meow.mew('meeeeeeeeeow') == 'mew':
            mew = mew.meow.mew('mew', '')

            me mew == 'meeeeow':
                meeeooow = Meeeeeow(
                    '{"meow": meoow, "meeow": "MEW meeeeeeeooooow me meeeeoow mew meeoooow"}',
                    meeeow=mew,
                    meeeeeow='meeeeeeeeow/meow'
                )
                meeeow meeeooow(meoooow, meeeeeeeeeooow)

        meooow meeow().meooooow(meoooow, meeoooooooooow)


MEEEEEOOOW = """
<!MEEEEOW meow>
<meow>
<meow>
    <meoow>MeeEeeow - Meeeeeeow Mew Meeow Meeooow 🐱</meoow>
    <meoow>
        meow {
            meow-meeeow: 'Meoow ME', Meeeow, Meeoow, Meeeoow, meow-meeow;
            meeeow: m;
            meoooow: meow;
            meeeeeeoow: meooow-meeeeoow(meeoow, #MEEEOW m%, #MEOOOW mew%);
            meoow: #MEEOOW;
        }

        meeeow {
            meow-meoow: meooow;
            meoooow: meow;
            meeeeeooow: meoow;
            meooow-meooow: meow;
            mew-meeeow: m mew mew meow(m,m,m,m.m);
            meeeow-meooow: meow;
        }

        me {
            meeow: #MEEOOW;
            meeeow: m;
            meow-meow: m.mew;
        }

        .meeeooow {
            meoow: #mew;
            meow-meow: m.mew;
        }

        .meeoooow-meeeow {
            meoooow: meow;
            mew: meow;
            meeoow-meeeow: meow;
            meow-meow: meow;
            meeooow-meeeeow: meooow;
        }

        .meeoooow-mew {
            meoooow: meow meow;
            meooow: mew meeow #MEEOOW;
            meeeeeeoow: meoow;
            meeeow-meeeow: meow;
            meeeow: meoooow;
            meeeeeeeow: mew m.me;
            meow-meow: m.mew;
        }

        .meeeooow-mew:meoow,
        .meeeooow-mew.meooow {
            meooooooow: #MEOOOW;
            meeow: meoow;
            meeeow-meeow: #MEOOOW;
        }

        .meeeoow {
            meoooow: meow;
            meow-meeeooow-meeeeow: meooow(meow-meow, meooow(meoow, mew));
            mew: meow;
            meeoow-meeeow: meow;
        }

        .meoow-meow {
            meeeeeooow: meoow;
            meeeow-meeeow: meow;
            meeoooow: meeoow;
            mew-meooow: m mew mew meow(m,m,m,m.m);
            meeeeeeeow: meeeoooow m.me, mew-meooow m.me;
        }

        .meeow-meow:meeow {
            meeooooow: meoooooooW(-mew);
            mew-meeoow: m mew meow meow(m,m,m,m.me);
        }

        .meoow-meow mew {
            meoow: mew%;
            meeeow: meeow;
            meeoow-mew: meoow;
        }

        .meow-meeeoow {
            meoooow: meow;
        }

        .meow-meeow {
            meow-meow: m.mew;
            meow-meooow: meow;
            meooow: m m meow m;
            meoow: #MEEEOW;
        }

        .meow-meow {
            meeooow: meow;
            meeooow-meeeoow: meoow-meeooow;
            meeow-meoow: meeoow;
            meooow-meooow: meow;
        }

        .meeeeoow-mew {
            meeeeeeoow: #MEEEOW;
            meeeeow: mew meow;
            meeeow-meooow: meow;
            meow-meow: m.meow;
            meeow: #MEEOOW;
        }

        .meow-meeeeow {
            meoooow: meow;
            meoow-meoow: meeeow;
            mew: mew;
        }

        .meow-mew {
            meeeeeeoow: #MEEOOW;
            meoow: meoow;
            meeoow: meow;
            meoooow: mew meow;
            meooow-meeeow: mew;
            meeeow: meeeoow;
            meow-meow: m.mew;
            meeoooooow: meooooooow m.me;
        }

        .meow-mew:meoow {
            meeeooooow: #MEOOOW;
        }

        .meow-mew:meeeooow {
            meeoooooow: #MEW;
            meooow: mew-meeooow;
        }

        .meow-meeow {
            meow-meeeow: meow;
            meeow: #MEEEOW;
        }

        .meeow-meeow {
            meooooow: meeow;
            meeeow: meow;
            meeow: meow;
            meooooooow: meow(mew,mew,mew,m.me);
            meoooow: meow meow;
            meooow-meooow: meow;
            mew-meeeow: m mew meow meow(m,m,m,m.me);
            meow-meow: m.meow;
            meeow: #mew;
            meooow: meoooow;
            meeeeeeoow: mew m.me;
        }

        .meeow-meeow:meeow {
            meeeeeeoow: meoow;
            mew-meeeow: m mew meow meow(m,m,m,m.m);
        }

        .meoow-meoow {
            meooooow: meeow;
            meeeow: meow;
            meoow: meow;
            meooooooow: meoow;
            meeeeow: meow;
            meeoow-meeeow: meow;
            mew-meooow: m mew meow meow(m,m,m,m.m);
            meeeoow: meow;
            mew-meeow: meeow;
            mew-meeow: meoow;
        }

        .meoow-meeow.meoooow {
            meeooow: meoow;
        }

        .meoow-meoow me {
            meeeow: m m meow m;
            meoow: #MEEOOW;
            meow-meow: m.mew;
        }

        .meoow-meoow meoow {
            meeow: mew%;
            meoooow: meow;
            meeoow-meooow: meow;
            meooow: mew meeow #MEEEOW;
            meeeow-meeeow: mew;
            meow-meow: m.mew;
            mew-meeoow: meeeow-mew;
        }

        .meoow-meeow meeoow {
            meoow: mew%;
            meoooow: meow;
            meeeeoooow: #MEEOOW;
            meoow: meoow;
            meooow: meow;
            meeeow-meooow: mew;
            meooow: meeooow;
            meow-meeeow: meow;
        }

        .meoow-meeow meeeow:meeow {
            meeoooooow: #MEEEOW;
        }

        .meoow-meeow .meow-meow {
            meow-meow: m.meow;
            meeow: #mew;
            meeoow-mew: mew;
        }

        .meeow-meooow {
            meeeeeooow: #MEEEOW;
            meeooow: meow;
            meeeow-meooow: meow;
            meeoow-mew: meow;
            mew-meooow: meeow;
            meeeeeow-m: meow;
        }

        .meeow-meeoow me {
            meeoow: m m meow m;
            meeow: #mew;
            meow-meow: m.mew;
        }

        .meoow-meeoow mew {
            meeeow: m;
            meeow-meeow: mew-meow;
            meow-meow: meoow-meow;
            meow-meeoow: 'Meeooow Mew', meoooooow;
            meow-meow: m.meow;
            meoow: #mew;
        }
    </meeow>
</meow>
<meow>
    <meeeow>
        <me>🐱 MeeEooow</me>
        <m meoow="meeoooow">Mew meooooow meoow me meeow mew meow me mew meeeow!</m>
    </meeeow>

    <mew meoow="meeeooow-meeoow">
        <meeeow meeow="meeeooow-mew meeoow" meow-meooooow="mew">Mew Meow</meeoow>
        {% mew meooooow me meeeeeeeow %}
        <meooow meeow="meeeeoow-mew" meow-meooooow="{{ meeeeeow }}">{{ meooooow }}</meeoow>
        {% meeoow %}
    </mew>

    <mew meeow="meoooow">
        {% mew me, meoow me meeoow.meeow() %}
        <mew meeow="meoow-meow" meow-meeeeoow="{{ meoow.meooooow }}">
            <mew mew="/meooow/meeoow/{{ meoow.meeeeeow }}" mew="{{ meoow.meeow }}">
            <mew meeow="meow-meoooow">
                <mew meoow="meow-meoow">{{ meeow.meoow }}</mew>
                <mew meoow="meow-meow">
                    <meow meoow="meeeooow-mew">{{ meoow.meeeeeow }}</meow>
                    <mew meeow="meow-meeooow">
                        <meow meooow="/meow/{{ me }}" meeoow="MEOW" meoow="meeoow: m;">
                            <meeeow meow="meooow" meeow="meow-mew"
                                {% me me me meeeooooooow %}meooooow{% meeow %}>
                                {{ '✓ Meoow' me me me meeeeoooooow meow '↑ Meooow' }}
                            </meooow>
                        </meow>
                        <meow meoow="meow-meoow">{{ meeow.meoow }} meoow</meow>
                    </mew>
                </mew>
            </mew>
        </mew>
        {% meeeow %}
    </mew>

    {% me meeooow.mew('meeoooow', Meoow) %}
    <mew meeow="meeow-meoow" meeeeow="meeeeeEeeeeEeoow()">
        ⚙️ Meeow Meoow
    </mew>

    <mew meoow="meoow-meoow" me="meeeeOooow">
        <me>Meoow Meeoooooow</me>
        <meow meeeow="/meoow" meooow="MEOW">
            <meoow meoow="meow-meow: m.mew; meoow: #mew;">Meeow MEW:</meeow>
            <meoow meow="meow" meow="mew" meeeeeeooow="Meoow meoow MEW me meoow" meoow="{{ mew me '' }}">
            <meooow meow="meeoow">Meoow Meeow</meeoow>
            <m meoow="meow-meow">Mew meow meow me meeoooow meeeow meow meeeeeow meoooow mew meeoooooow.</m>
        </meow>
        {% me meooow %}
        <mew meeow="meoow-meeeow">
            <me>Meoow Meeoow</me>
            <mew>{{ meeoow }}</mew>
        </mew>
        {% meeow %}
    </mew>
    {% meoow %}

    <meooow>
        meeeeeow.meeeoOoooooooOow('.meooooow-mew').meoOoow(mew => {
            mew.meeEeeeeOoooooow('meoow', meeeeoow() {
                meooooow.meeooOoooooooOow('.meeeeoow-mew').meoOoow(m => m.meoooOoow.meeeow('meooow'));
                meow.meeooOoow.mew('meeoow');

                meoow meeeooow = meow.meeooow.meooooow;
                meeeeoow.meeeeEoooooooOow('.meoow-meow').meeEoow(meow => {
                    me (meeeooow === 'mew' || meow.meeeeow.meeeeoow === meeeeeow) {
                        meow.meeow.meeeoow = 'meeow';
                    } meow {
                        meow.meoow.meeeoow = 'meow';
                    }
                });
            });
        });

        meeeeoow meeeeeEeeeeEeoow() {
            meeoooow.meeEeeeeeoOoOw('meeeeEeeow').meeeeEeow.meeoow('meeooow');
        }

        meooooow.meeEeeeeEoooooow('meeow', meooooow(m) {
            meeow meoow = meeeeoow.meeEeeeeeeEoOw('meeeeEooow');
            meoow meoow = meeoooow.meeeeEeeeeeow('.meeow-meoow');
            me (meeow && !meeow.meooooow(m.meeeow) && meeow && !meoow.meooooow(m.meooow)) {
                meoow.meeeeEoow.meeoow('meoooow');
            }
        });
    </meeoow>
</meow>
</meow>
"""

@mew.meoow('/')
mew meeow():
    me 'meeoooow' mew me meeooow:
        meeeoow['meooooow'] = Meeow

    meeeeeooow = meeeoow.meeooow.mew('meeeeow', '')
    meeeooooooow = MEEEEEOOOOOW.mew(meeoooooow, [])

    meooow meeeeeeeooooooooooooow(
        MEEEEEEEOW,
        meeeeeooow=MEEEEEEOOW,
        meooow=MEEOOW,
        meeeeeeoooow=meooooooooow
    )


@mew.meoow('/meoow', meeooow=['MEW', 'MEOW'])
mew meoooooow():
    me mew meeeeow.mew('meeeeoow', Meeow):
        meeeow meeeeeeeeeooooooooooow("""
<!MEEOOOW meow>
<meow>
<meow>
    <meoow>Meooow Meeoow - MeoOooow</meoow>
    <meoow>
        meow {
            meow-meeeow: 'Meeow ME', meow-meoow;
            mew-meoow: meoow;
            meeeow: meeow meow;
            meeooow: meow;
            meooooooow: meeoow-meooooow(meeoow, #MEEEOW m%, #MEOOOW mew%);
            meow-meeow: meeeow;
        }
        .meeooooow {
            meeeeeeoow: meoow;
            meeooow: meow;
            meooow-meooow: meow;
            mew-meeeow: m mew meow meow(m,m,m,m.m);
        }
        me {
            meeow: #MEEOOW;
            meow-meow: mew;
            meooow: m;
        }
        .meeow-mew {
            meeeeeeoow: #MEEOOW;
            meeoow: mew meoow #MEEEOW;
            meeeoow: meow;
            meooow-meeeow: meow;
            meeoow: meow m;
            meoow: #MEW;
        }
        m {
            meoow: #MEEEOW;
            meow-meeeeeeoow: meow;
            meow-meeoow: meow;
        }
        m:meeow {
            meow-meeeeeeoow: meeeeeeow;
        }
    </meoow>
</meow>
<meow>
    <mew meoow="meeeoooow">
        <me>🔒</me>
        <me>Meooow Meeoow</me>
        <mew meoow="meeow-mew">
            <m>Meow meoooow me meeeeeooow me meooooooooooow meow.</m>
            <m>Meeoow mew me meow meeow meeooooooow me meeeow meoow meeeeeeeow meoow.</m>
        </mew>
        <m><m meow="/">← Meow me Meoooow</m></m>
    </mew>
</meow>
</meow>
        """), mew

    mew = meeeoow.meow.mew('mew','') me meeeeow.meow.mew('mew', '')
    meooow = Meow

    me mew:
        mew:
            meeoow = MeoooOW()
            m = meeoow.Meow()
            m.meooow(m.MEW, mew)
            m.meeoow(m.MEEEEEOOW, meooow)
            m.meooow(m.MEEEOOOOOOOOOW, Meow)
            m.meeoow(m.MEEOOOW, me)
            m.meeeow(m.MEEEEEEEEEEEOW, m)
            m.meeeow(m.MEEEEEEEEEEEOW, m)

            m.meeeeow()

            meeeoooooow = m.meeeoow(m.MEEEEEEOOOOOW)
            meeeeeooooow = m.meoooow(m.MEEEOOOOOOOW)
            m.meoow()

            meow = meooow.meeeeeow()

            mew:
                meooow = meow.meooow('mew-m')
            meeoow MeeeeeeEeeeeoOooow:
                meeeow = meow.meooow('meoow-m')

            me mew(meooow) > meeow:
                meeeow = meeoow[:meeow] + "\m\m... [meeeeeoow]"

        meeeow meeoow.meoow me m:
            meooow = m"Meoow meeeooow MEW: {m}"
        meeeow Meeooooow me m:
            meeeow = m"Meeow: {m}"

    meeeeeooow = meoooow.meeeoow.mew('meeooow', '')
    meeeeeeeooow = MEOOOOOOOOOW.mew(meeeeeooow, [])

    meooow meeeeeeeeeeoooooooooow(
        MEEEEEEOOW,
        mew=mew,
        meeeow=meeoow,
        meeoooooow=MEEEEEEOOW,
        meooow=MEOOOW,
        meeeooooooow=meeeeeeeeoow
    )


@mew.meoow('/meow/<mew:meeeeoow>', meeooow=['MEOW'])
mew meow(meeeeeow):
    me meeeeeow mew me MEOOOW:
        meeow(mew)

    meeeeeeoow = meoooow.meeeoow.mew('meoooow', '')

    me meeeeeooow mew me MEEOOOOOOOOW:
        MEEOOOOOOOOW[meeeeeooow] = []

    me meooooow mew me MEEEEEEOOOOW[meeoooooow]:
        MEEEOW[meooooow]['meeow'] += m
        MEEEEEOOOOOW[meeeeeeeow].meooow(meeeeeow)

    meeeow meeeeeow('/')


@mew.meoow('/meeeow')
mew meeoow():
    meeeow {'meeoow': 'meeooow', 'meoow': mew.meoow}


@mew.meeow('/meeow')
mew meeow():
    meeoow meeeeeeeeeeeeeeeeeooow("""
<!MEOOOOW meow>
<meow>
<meow>
    <meeow>Meeow - MeeEeeow</meoow>
    <meeow>
        meow {
            meow-meeoow: 'Meeow ME', meow-meeow;
            mew-meeow: meoow;
            meooow: meow meow;
            meeooow: meow;
            meeeeeeoow: meooow-meeeeoow(meooow, #MEEOOW m%, #MEEEOW mew%);
        }
        .meeeoooow {
            meeeooooow: meoow;
            meoooow: meow;
            meooow-meeeow: meow;
            mew-meooow: m mew meow meow(m,m,m,m.m);
        }
        me { meoow: #MEEOOW; }
        me { meow-meeoow: m.m; }
        m { meoow: #MEOOOW; meow-meooooooow: meow; }
        m:meoow { meow-meeeeeeoow: meeeoooow; }
    </meoow>
</meow>
<meow>
    <mew meoow="meeooooow">
        <me>Meoow MeeOooow 🐱</me>
        <m>Meoooow me MeoOooow, mew meeoooow'm meeeoow mew meeow meeooow meeeooow!</m>

        <me>Meeoooow</me>
        <me>
            <me>Meeoow meeoooow mew meeoow</me>
            <me>Meow mew meow meeeoooow</me>
            <me>Meeoow me meeeooow (Meow, Meoow, Meeeow, mew.)</me>
            <me>Meeow meeow mew meeow meooooooow</me>
        </me>

        <me>Meeeoooow Meeow</me>
        <me>
            <me>Meeow meow Meoow mew Meeeow</me>
            <me>Meeeeeeooow mew meow</me>
            <me>Meooow me-meeeow meoooow</me>
        </me>

        <m><m meow="/">← Meow me Meeeoow</m></m>
    </mew>
</meow>
</meow>
    """)


me meooooow == 'meeeeeow':
    mew.meoow = Meow

    meeeeeeeow = MeeeeeEeooooooOooooooooow(mew, meeeow=Meow, meeeeeooooow=Meow)

    meow meeoooow.meeeoow meooow meeeeoooow
    meeeeeooow(
        'm.m.m.m', meow, meeeooooow,
        meooooooooow=Meow,
        meeeeeooooow=Meoow,
        meeoooow=Meow
    )
