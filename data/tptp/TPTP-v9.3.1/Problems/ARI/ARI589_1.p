%------------------------------------------------------------------------------
% File     : ARI589_1 : TPTP v9.3.1. Released v5.1.0.
% Domain   : Arithmetic
% Problem  : There is a number different from Y and Z
% Version  : Especial.
% English  :

% Refs     : [Wal10] Waldmann (2010), Email to Geoff Sutcliffe
% Source   : [Wal10]
% Names    :

% Status   : Theorem
% Rating   : 0.00 v9.3.0, 0.25 v9.1.0, 0.38 v9.0.0, 0.25 v8.2.0, 0.12 v8.1.0, 0.25 v7.5.0, 0.30 v7.4.0, 0.12 v7.3.0, 0.17 v7.0.0, 0.29 v6.4.0, 0.00 v6.3.0, 0.29 v6.2.0, 0.50 v6.1.0, 0.44 v6.0.0, 0.43 v5.5.0, 0.44 v5.4.0, 0.50 v5.3.0, 0.60 v5.2.0, 0.50 v5.1.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   2 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    3 (   2   ~;   0   |;   1   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    6 (   6 avg)
%            Maximal term depth    :    1 (   1 avg)
%            Number arithmetic     :    3 (   0 atm;   0 fun;   0 num;   3 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    1 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    0 (   0 usr;   0 con; --- aty)
%            Number of variables   :    3 (   2   !;   1   ?;   3   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(exists_X_noteq_Y_Z,conjecture,
    ! [Y: $int,Z: $int] :
    ? [X: $int] :
      ( ( Y != X )
      & ( Z != X ) ) ).

%------------------------------------------------------------------------------
