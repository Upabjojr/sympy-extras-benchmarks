%------------------------------------------------------------------------------
% File     : ARI722_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : If floor(X) = X, then X is an integer
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 0.40 v9.3.0, 0.38 v9.1.0, 0.50 v9.0.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.50 v7.3.0, 0.67 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   1 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    3 (   3 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    3 (   1 atm;   1 fun;   0 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 1-2 aty)
%            Number of functors    :    1 (   0 usr;   0 con; 1-1 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(prove,conjecture,
    ! [X: $real] :
      ( ( X = $floor(X) )
     => $is_int(X) ) ).

%------------------------------------------------------------------------------
