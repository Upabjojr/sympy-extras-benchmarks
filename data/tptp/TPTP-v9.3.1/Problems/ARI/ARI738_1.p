%------------------------------------------------------------------------------
% File     : ARI738_1 : TPTP v9.3.1. Released v7.0.0.
% Domain   : Arithmetic
% Problem  : Integer of ceiling of real compared to real of integer or real
% Version  : Especial.
% English  :

% Refs     : [Pas16] Paskevich (2016), Email to Geoff Sutcliffe
% Source   : [Pas16]
% Names    : intreal-IntReal-G7.p [Pas16]

% Status   : Theorem
% Rating   : 0.40 v9.3.0, 0.50 v9.1.0, 0.62 v8.2.0, 0.88 v7.5.0, 0.60 v7.4.0, 0.62 v7.3.0, 0.67 v7.0.0
% Syntax   : Number of formulae    :    1 (   0 unt;   0 typ;   0 def)
%            Number of atoms       :    2 (   1 equ)
%            Maximal formula atoms :    2 (   2 avg)
%            Number of connectives :    2 (   1   ~;   0   |;   0   &)
%                                         (   0 <=>;   1  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    3 (   2 avg)
%            Number arithmetic     :    7 (   1 atm;   5 fun;   0 num;   1 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    0 (   0   >;   0   *;   0   +;   0  <<)
%            Number of predicates  :    2 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    3 (   0 usr;   0 con; 1-1 aty)
%            Number of variables   :    1 (   1   !;   0   ?;   1   :)
% SPC      : TF0_THM_EQU_ARI_NDT

% Comments :
%------------------------------------------------------------------------------
tff(g7,conjecture,
    ! [X: $real] :
      ( $less($to_int(X),$to_int($ceiling(X)))
     => ( $to_real($to_int(X)) != X ) ) ).

%------------------------------------------------------------------------------
