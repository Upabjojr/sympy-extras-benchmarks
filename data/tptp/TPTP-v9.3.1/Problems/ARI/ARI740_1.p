%------------------------------------------------------------------------------
% File     : ARI740_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Arithmetic
% Problem  : Integer power of real
% Version  : Especial.
% English  :

% Refs     : [Pas16] Paskevich (2016), Email to Geoff Sutcliffe
% Source   : [Pas16]
% Names    : real-PowerIntTest-Pow_2_2.p [Pas16]

% Status   : Theorem
% Rating   : 0.20 v9.3.0, 0.25 v8.2.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.38 v7.3.0, 0.33 v7.0.0
% Syntax   : Number of formulae    :   10 (   3 unt;   1 typ;   0 def)
%            Number of atoms       :   18 (   8 equ)
%            Maximal formula atoms :    3 (   2 avg)
%            Number of connectives :    9 (   0   ~;   0   |;   1   &)
%                                         (   0 <=>;   8  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   4 avg)
%            Maximal term depth    :    4 (   1 avg)
%            Number arithmetic     :   54 (  10 atm;   9 fun;  18 num;  17 var)
%            Number of types       :    2 (   0 usr;   2 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   1   >;   1   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :   10 (   1 usr;   6 con; 0-2 aty)
%            Number of variables   :   17 (  17   !;   0   ?;  17   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(power,type,
    power: ( $real * $int ) > $real ).

tff(power_0,axiom,
    ! [X: $real] : ( power(X,0) = 1.0 ) ).

tff(power_s,axiom,
    ! [X: $real,N: $int] :
      ( $lesseq(0,N)
     => ( power(X,$sum(N,1)) = $product(X,power(X,N)) ) ) ).

tff(power_s_alt,axiom,
    ! [X: $real,N: $int] :
      ( $less(0,N)
     => ( power(X,N) = $product(X,power(X,$difference(N,1))) ) ) ).

tff(power_1,axiom,
    ! [X: $real] : ( power(X,1) = X ) ).

tff(power_sum,axiom,
    ! [X: $real,N: $int,M: $int] :
      ( $lesseq(0,N)
     => ( $lesseq(0,M)
       => ( power(X,$sum(N,M)) = $product(power(X,N),power(X,M)) ) ) ) ).

tff(power_mult,axiom,
    ! [X: $real,N: $int,M: $int] :
      ( $lesseq(0,N)
     => ( $lesseq(0,M)
       => ( power(X,$product(N,M)) = power(power(X,N),M) ) ) ) ).

tff(power_mult2,axiom,
    ! [X: $real,Y: $real,N: $int] :
      ( $lesseq(0,N)
     => ( power($product(X,Y),N) = $product(power(X,N),power(Y,N)) ) ) ).

tff(pow_ge_one,axiom,
    ! [X: $real,N: $int] :
      ( ( $lesseq(0,N)
        & $lesseq(1.0,X) )
     => $lesseq(1.0,power(X,N)) ) ).

tff(pow_2_2,conjecture,
    power(2.0,2) = 4.0 ).

%------------------------------------------------------------------------------
