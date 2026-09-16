%------------------------------------------------------------------------------
% File     : ARI612_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Interval (8,12) is contained in (5,15)
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.3.0, 0.12 v7.1.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.33 v6.0.0, 0.38 v5.4.0, 0.50 v5.3.0, 0.43 v5.2.0, 0.60 v5.1.0
% Syntax   : Number of formulae    :    3 (   0 unt;   2 typ;   0 def)
%            Number of atoms       :    8 (   0 equ)
%            Maximal formula atoms :    8 (   8 avg)
%            Number of connectives :    7 (   0   ~;   0   |;   3   &)
%                                         (   2 <=>;   2  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    1 (   1 avg)
%            Number arithmetic     :   11 (   4 atm;   0 fun;   4 num;   3 var)
%            Number of types       :    2 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   2   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   2 usr;   0 prp; 1-2 aty)
%            Number of functors    :    4 (   0 usr;   4 con; 0-0 aty)
%            Number of variables   :    3 (   3   !;   0   ?;   3   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(p_type,type,
    p: $int > $o ).

tff(q_type,type,
    q: $int > $o ).

tff(interv_8_12_subset_5_15,conjecture,
    ( ( ! [X: $int] :
          ( ( $less(5,X)
            & $less(X,15) )
        <=> p(X) )
      & ! [X: $int] :
          ( ( $less(8,X)
            & $less(X,12) )
        <=> q(X) ) )
   => ! [X: $int] :
        ( q(X)
       => p(X) ) ) ).

%------------------------------------------------------------------------------
