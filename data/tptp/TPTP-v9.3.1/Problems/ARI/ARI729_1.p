%------------------------------------------------------------------------------
% File     : ARI729_1 : TPTP v9.3.1. Released v6.3.0.
% Domain   : Arithmetic
% Problem  : If floor(X)=floor(Y), the X-Y < 1
% Version  : Especial.
% English  :

% Refs     : [Wal14] Waldmann (2014), Email to Geoff Sutcliffe
% Source   : [Wal14]
% Names    : 

% Status   : Theorem
% Rating   : 0.40 v9.3.0, 0.38 v7.5.0, 0.40 v7.4.0, 0.50 v7.3.0, 0.67 v7.0.0, 0.43 v6.4.0, 0.33 v6.3.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   1 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    1 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number arithmetic     :    7 (   1 atm;   3 fun;   1 num;   2 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   0 usr;   1 con; 0-2 aty)
%            Number of variables   :    2 (   2   !;   0   ?;   2   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(prove,conjecture,
    ! [X: $real,Y: $real] :
      ( ( $floor(X) = $floor(Y) )
     => $less($difference(X,Y),1.0) ) ).

%------------------------------------------------------------------------------
