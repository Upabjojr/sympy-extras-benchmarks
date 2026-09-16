%------------------------------------------------------------------------------
% File     : ARI762_1 : TPTP v9.3.1. Released v9.1.0.
% Domain   : Arithmetic
% Problem  : Maximal function
% Version  : Especial.
% English  :

% Refs     : [KK+16] Kotelnikov et al. (2016), The Vampire and the FOOL
%          : [Kot18] Kotelnikov (2018), Email to Geoff Sutcliffe
% Source   : [Kot18]
% Names    : if-then-else [Kot18]

% Status   : Theorem
% Rating   : ? v9.1.0
% Syntax   : Number of formulae    :    3 (   1 unt;   1 typ;   0 def)
%            Number of atoms       :    5 (   2 equ)
%            Maximal formula atoms :    3 (   2 avg)
%            Number of connectives :    0 (   0   ~;   0   |;   0   &)
%                                         (   0 <=>;   0  =>;   0  <=;   0 <~>)
%            Maximal formula depth :    4 (   4 avg)
%            Maximal term depth    :    2 (   1 avg)
%            Number of FOOLs       :    1 (   1 fml;   0 var)
%            Number of X terms     :    2 (   0  [];   2 ite;   0 let;   0 dis)
%            Number arithmetic     :    7 (   3 atm;   0 fun;   0 num;   4 var)
%            Number of types       :    1 (   0 usr;   1 ari;   0 dat;   0 cdt)
%            Number of type conns  :    2 (   1   >;   1   *;   0   +;   0  <<)
%            Number of predicates  :    3 (   0 usr;   0 prp; 2-2 aty)
%            Number of functors    :    1 (   1 usr;   0 con; 2-2 aty)
%            Number of variables   :    4 (   4   !;   0   ?;   4   :)
% SPC      : TX0_THM_EQU_ARI_NDT

% Comments : 
%------------------------------------------------------------------------------
tff(max,type,
    max: ( $int * $int ) > $int ).

tff(max_definition,axiom,
    ! [X: $int,Y: $int] :
      ( max(X,Y) = $ite($less(X,Y),Y,X) ) ).

tff(max_conjecture,conjecture,
    ! [X: $int,Y: $int] :
      $ite(max(X,Y) = X,$greatereq(X,Y),$greatereq(Y,X)) ).

%------------------------------------------------------------------------------
