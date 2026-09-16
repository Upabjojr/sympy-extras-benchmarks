%------------------------------------------------------------------------------
% File     : ARI585_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : Interval (X+5,X+8) is covered by (Y,Y+4), e.g. for Y = X + 5
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v7.4.0, 0.17 v7.3.0, 0.25 v7.1.0, 0.17 v7.0.0, 0.00 v6.2.0, 0.20 v6.1.0, 0.44 v6.0.0, 0.50 v5.5.0, 0.38 v5.4.0, 0.50 v5.3.0, 0.57 v5.2.0, 0.80 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    4 (   0 equ)
%            Maximal formula atoms :    4 (   4 avg)
%            Number of connectives :    3 (   0   ~;   0   |;   2   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :   13 (   4 atm;   3 fun;   3 num;   3 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    4 (   0 usr;   3 con; 0-2 aty)
%            Number of variables   :    3 (   2   !;   1   ?;   3   :)
% SPC      : TF0_THM_NEQ_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(interv_4_can_cover_interv_3,conjecture,
    ! [X: $int] :
    ? [Y: $int] :
    ! [Z: $int] :
      ( ( $less($sum(X,5),Z)
        & $less(Z,$sum(X,8)) )
     => ( $less(Y,Z)
        & $less(Z,$sum(Y,4)) ) ) ).

%------------------------------------------------------------------------------
