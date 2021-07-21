from mininet.topo import Topo

class MyTopo( Topo ):
    "Simple topology example."

    def build( self ):
        "Create custom topo."

        # Add hosts and switches
	h11 = self.addHost( 'h11' )
        h12 = self.addHost( 'h12' )

	h21 = self.addHost( 'h21' )
	h22 = self.addHost( 'h22' )

	h31 = self.addHost( 'h31' )
	h32 = self.addHost( 'h32' )

	h41 = self.addHost( 'h41' )
	h42 = self.addHost( 'h42' )



        s1 = self.addSwitch( 's1' )
        s2 = self.addSwitch( 's2' )
        s3 = self.addSwitch( 's3' )
        s4 = self.addSwitch( 's4' )
        s5 = self.addSwitch( 's5' )
        s6 = self.addSwitch( 's6' )
        s5 = self.addSwitch( 's5' )

        # Add links
        self.addLink( h11, s1 )
        self.addLink( h12, s1 )

        self.addLink( h21, s2 )
        self.addLink( h22, s2 )

        self.addLink( h31, s3 )
        self.addLink( h32, s3 )

        self.addLink( h41, s4 )
        self.addLink( h42, s4 )

	self.addLink( s1, s2 )
	self.addLink( s3, s4 )

	self.addLink( s1, s5 )
	self.addLink( s2, s5 )

	self.addLink( s3, s6 )
	self.addLink( s4, s6 )

	self.addLink( s5, s6 )
topos = { 'mytopo': ( lambda: MyTopo() ) }
