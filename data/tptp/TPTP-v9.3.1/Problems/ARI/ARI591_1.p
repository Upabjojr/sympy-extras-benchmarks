%------------------------------------------------------------------------------
% File     : ARI591_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : There is an X in the interval (0,3) that is different from Y
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.12 v7.5.0, 0.20 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.00 v6.3.0, 0.29 v6.2.0, 0.38 v6.1.0, 0.44 v6.0.0, 0.43 v5.5.0, 0.33 v5.4.0, 0.50 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    3 (   1 equ)
%            Maximal formula atoms :    3 (   3 avg)
%            Number of connectives :    3 (   1   ~;   0   |;   2   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    1 (   1 avg)
%            Number arithmetic     :    6 (   2 atm;   0 fun;   2 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    2 (   0 usr;   2 con; 0-0 aty)
%            Number of variables   :    2 (   1   !;   1   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(exists_X_0_3_noteq_Y,conjecture,
    ! [Y: $int] :
    ? [X: $int] :
      ( $less(0,X)
      & $less(X,3)
      & ( Y != X ) ) ).

%------------------------------------------------------------------------------
